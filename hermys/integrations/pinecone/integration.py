from pinecone import ServerlessSpec  # type: ignore
from pinecone.grpc import PineconeGRPC as Pinecone  # type: ignore

from hermys.settings import get_settings

settings = get_settings()


class PineconeIntegration:
    def __init__(self) -> None:
        self.pc = Pinecone(api_key='1aac72b8-e184-44da-bcb4-53f421137acf')
        self.spec = ServerlessSpec(
            cloud=settings.PINECONE_CLOUD,
            region=settings.PINECONE_REGION,
        )

    def create_index(self, *, index_name: str):
        if index_name not in self.pc.list_indexes().names():
            return self.pc.create_index(
                name=index_name,
                dimension=1536,
                metric='cosine',
                spec=self.spec,
            )

        # TODO: Construir uma exceção customizada
        raise Exception()

    def delete_index(self, *, index_name: str):
        if index_name not in self.pc.list_indexes().names():
            return self.pc.delete_index(name=index_name)

        # TODO: Construir uma exceção customizada
        raise Exception()
