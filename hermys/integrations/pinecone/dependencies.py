from typing import Annotated

from fastapi import Depends

from hermys.integrations.pinecone.integration import PineconeIntegration


def get_pinecone_integration():
    return PineconeIntegration()


GetPineconeIntegration = Annotated[
    PineconeIntegration,
    Depends(get_pinecone_integration),
]
