import os

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import (
    create_history_aware_retriever,
)
from langchain.chains.retrieval import create_retrieval_chain
from langchain.pydantic_v1 import SecretStr
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_mongodb import MongoDBChatMessageHistory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone  # type: ignore

from hermys.modules.clerk.schemas import ClerkRetrieve
from hermys.modules.knowledge.schemas import KnowledgeRetrieve
from hermys.modules.organization.schemas import OrganizationRetrieve
from hermys.settings import get_settings

settings = get_settings()

os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_API_KEY'] = settings.LANGCHAIN_API_KEY


class RAGService:
    def __init__(
        self,
        *,
        knowledge: KnowledgeRetrieve,
        clerk: ClerkRetrieve,
        organization: OrganizationRetrieve,
    ):
        os.environ['LANGCHAIN_PROJECT'] = organization.name
        self.knowledge = knowledge
        self.clerk = clerk
        self.organization = organization

        self.namespace = str(knowledge.id)
        self.index_name = organization.name

        self.pinecone = Pinecone(api_key=settings.PINECONE_API_KEY)

        self.llm = ChatOpenAI(
            api_key=SecretStr(settings.OPENAI_API_KEY),
            model=clerk.gpt_model,
            temperature=0,
        )
        self.embeddings = OpenAIEmbeddings(
            api_key=SecretStr(settings.OPENAI_API_KEY),
            model='text-embedding-ada-002',
        )

    def invoke(self, *, session_id: str, quiestion: str) -> str:
        vectorstore = PineconeVectorStore(
            pinecone_api_key=settings.PINECONE_API_KEY,
            index_name=self.index_name,
            namespace=self.namespace,
            embedding=self.embeddings,
        )
        retriever = vectorstore.as_retriever(
            search_type='similarity_score_threshold',
            search_kwargs={'k': self.knowledge.top_k, 'score_threshold': 0.7},
        )

        contextualize_q_system_prompt = """Given a chat history and the \
        latest user question which might reference context in the chat \
        history, formulate a standalone question which can be understood \
        without the chat history. Do NOT answer the question, \
        just reformulate it if needed and otherwise return it as is."""
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ('system', contextualize_q_system_prompt),
                MessagesPlaceholder('chat_history'),
                ('human', '{input}'),
            ]
        )
        history_aware_retriever = create_history_aware_retriever(
            self.llm, retriever, contextualize_q_prompt
        )

        ### Answer question ###
        qa_system_prompt = self._get_prompt(
            clerk=self.clerk,
            knowledge=self.knowledge,
        )

        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ('system', qa_system_prompt),
                MessagesPlaceholder('chat_history'),
                ('human', '{input}'),
            ]
        )
        question_answer_chain = create_stuff_documents_chain(
            self.llm, qa_prompt
        )

        rag_chain = create_retrieval_chain(
            history_aware_retriever, question_answer_chain
        )

        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,  # type: ignore
            self._get_session_history,
            input_messages_key='input',
            history_messages_key='chat_history',
            output_messages_key='answer',
        )

        result = conversational_rag_chain.invoke(
            {'input': quiestion},
            config={'configurable': {'session_id': session_id}},
        )['answer']

        return result

    def _get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        return MongoDBChatMessageHistory(
            connection_string=settings.MONGODB_URI,
            database_name=f'org-{self.organization.name}',
            collection_name='chat-history',
            session_id=f'{str(self.knowledge.id)}:{session_id}',
        )

    def _get_prompt(
        self,
        *,
        clerk: ClerkRetrieve,
        knowledge: KnowledgeRetrieve,
    ):
        prompt = clerk.prompt.format(
            KNOWLEDGE=knowledge.prompt_copmlement,
            CONTEXT='{context}',
        )
        return prompt
