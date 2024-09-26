from typing import Annotated, List

from bson import ObjectId
from fastapi import Depends
from langchain.pydantic_v1 import SecretStr
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec  # type: ignore

from hermys.modules.knowledge.dependencies import GetKnowledgeRepository
from hermys.modules.knowledge.respository import KnowledgeRepository
from hermys.modules.knowledge.schemas import KnowledgeRetrieve
from hermys.settings import get_settings

settings = get_settings()


class KnowledgeTrainService:
    def __init__(self, knowledge_repo: KnowledgeRepository) -> None:
        self.knowledge_repo = knowledge_repo
        self.embeddings = OpenAIEmbeddings(
            api_key=SecretStr(settings.OPENAI_API_KEY),
            model='text-embedding-ada-002',
        )
        self.pinecone = Pinecone(api_key=settings.PINECONE_API_KEY)

    async def dispatch(self, knowledge_id: str, index_name: str):
        knowledge = await self._get_knowledge(knowledge_id=knowledge_id)

        await self._configure_index(index_name=index_name)

        if await self._is_knowledge_trained(
            index_name=index_name,
            namespace=knowledge_id,
        ):
            await self._delete_knowledge_trainament(
                index_name=index_name,
                namespace=knowledge_id,
            )

        await self._train_knowledge(knowledge=knowledge, index_name=index_name)

    async def _get_knowledge(self, *, knowledge_id: str):
        return await self.knowledge_repo.get_or_rise(
            by='_id',
            value=ObjectId(knowledge_id),
        )

    async def _configure_index(self, *, index_name: str):
        spec = ServerlessSpec(
            cloud=settings.PINECONE_CLOUD,
            region=settings.PINECONE_REGION,
        )

        if index_name not in self.pinecone.list_indexes().names():
            self.pinecone.create_index(
                name=index_name,
                dimension=1536,
                spec=spec,
                metric='cosine',
            )

    async def _is_knowledge_trained(
        self,
        *,
        index_name: str,
        namespace: str,
    ):
        index = self.pinecone.Index(name=index_name)
        index_stats = index.describe_index_stats()

        if namespace in index_stats.get('namespaces', {}):
            return True

        return False

    async def _delete_knowledge_trainament(
        self,
        *,
        index_name: str,
        namespace: str,
    ):
        index = self.pinecone.Index(name=index_name)

        index.delete(namespace=namespace, delete_all=True)

    async def _train_knowledge(
        self,
        *,
        knowledge: KnowledgeRetrieve,
        index_name: str,
    ):
        loader = PyPDFLoader(file_path=knowledge.pdf_url)
        import re

        def clean_text(text: str):
            text = re.sub(r'(?<!\n)\n(?!\n[A-Z])', ' ', text)
            text = re.sub(r'\s+', ' ', text)
            return text.strip()

        documents = loader.load()
        cleaned_documents: List[Document] = []
        for doc in documents:
            cleaned_text = clean_text(doc.page_content)
            doc.page_content = cleaned_text
            cleaned_documents.append(doc)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=knowledge.chunk_size,
            chunk_overlap=knowledge.chunk_overlap,
        )
        splits = text_splitter.split_documents(cleaned_documents)

        vectorstore = PineconeVectorStore(
            pinecone_api_key=settings.PINECONE_API_KEY,
            index_name=index_name,
            namespace=str(knowledge.id),
            embedding=self.embeddings,
        )
        vectorstore.add_documents(splits)


def get_knowledge_train_service(knowledge_repo: GetKnowledgeRepository):
    return KnowledgeTrainService(knowledge_repo=knowledge_repo)


GetKnowledgeTrainService = Annotated[
    KnowledgeTrainService,
    Depends(get_knowledge_train_service),
]
