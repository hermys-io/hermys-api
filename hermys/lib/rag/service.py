import os

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import (
    create_history_aware_retriever,
)
from langchain.chains.retrieval import create_retrieval_chain
from langchain.pydantic_v1 import SecretStr
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_mongodb import MongoDBChatMessageHistory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec  # type: ignore

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
            search_kwargs={'k': self.knowledge.top_k, 'score_threshold': 0.9},
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
        qa_system_prompt = """Você é um assistente especializado em responder \
        perguntas. Todas as suas respostas devem parecer humanas e você não \
        deve dizer que é um assistente virtual ou algo similar. Use o \
        contexto fornecido para responder à pergunta. Seja conciso e responda \
        em até três frases que se assemelhem a respostas humanas. Suas \
        respostas devem estar em português do Brasil. Se você não souber a \
        resposta, simplesmente diga que não sabe e peça ao usuário para \
        enviar um e-mail para a organização. Se a pergunta for sobre o \
        endereço, local ou horário da prova, informe que o local aparecerá no \
        cartão de inscrição dentro do período estabelecido no cronograma de \
        atividades. Sempre que for questionado sobre as datas, se não souber, \
        informe que o cronograma presente no site da organização tem todas as \
        informações referentes às datas. Lembre-se de informar ao candidato \
        que a informação está presente no edital. Caso perguntem se é \
        necessário residir no local para algum cargo, informe que apenas para \
        o cargo de Agente Comunitário de Saúde (ACS) o candidato deve residir \
        na área da comunidade em que atuará.\

        CONTEXTO: \
        {context}"""
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

    async def train(self):
        loader = PyPDFLoader(file_path=self.knowledge.pdf_url)

        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.knowledge.chunk_size,
            chunk_overlap=self.knowledge.chunk_overlap,
        )
        splits = text_splitter.split_documents(docs)

        self._pinecone_configure_index()

        vectorstore = PineconeVectorStore(
            pinecone_api_key=settings.PINECONE_API_KEY,
            index_name=self.index_name,
            namespace=self.namespace,
            embedding=self.embeddings,
        )
        vectorstore.add_documents(splits)

    def _get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        return MongoDBChatMessageHistory(
            connection_string=settings.MONGODB_URI,
            database_name=f'org-{self.organization.name}',
            collection_name='chat-history',
            session_id=f'{str(self.knowledge.id)}:{session_id}',
        )

    def _pinecone_configure_index(self):
        spec = ServerlessSpec(
            cloud=settings.PINECONE_CLOUD,
            region=settings.PINECONE_REGION,
        )

        if self.index_name not in self.pinecone.list_indexes().names():
            self.pinecone.create_index(
                name=self.index_name,
                dimension=1536,
                spec=spec,
                metric='cosine',
            )
