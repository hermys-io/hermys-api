import json

from bson import ObjectId
from fastapi import APIRouter

from hermys.common.host_name_dependencies import GetHostName
from hermys.db.host_db import GetHostDB
from hermys.db.shared_db import GetSharedDB
from hermys.lib.rag.service import RAGService
from hermys.modules.clerk.repository import ClerkRepository
from hermys.modules.knowledge.dependencies import GetHostKnowledgeService
from hermys.modules.knowledge.respository import KnowledgeRepository
from hermys.modules.organization.repository import OrganizationRepository

router = APIRouter()


@router.get('/', status_code=200)
async def list_knowledge(
    clerk_slug: str,
    knowledge_service: GetHostKnowledgeService,
):
    results = await knowledge_service.list(clerk_slug=clerk_slug)

    return [result.model_dump() for result in results]


@router.get('/ask', status_code=200)
async def ask(
    db: GetSharedDB,
    host_db: GetHostDB,
    host_name: GetHostName,
    knowledge_id: str,
    question: str,
    session_id: str,
):
    organization_repo = OrganizationRepository(db=db)
    knowledge_repo = KnowledgeRepository(db=host_db)
    clerk_repo = ClerkRepository(db=host_db)

    organization = await organization_repo.get_or_rise(
        by='host',
        value=host_name,
    )
    knowledge = await knowledge_repo.get_or_rise(
        by='_id',
        value=ObjectId(knowledge_id),
    )
    clerk = await clerk_repo.get_or_rise(
        by='_id',
        value=knowledge.clerk,
    )

    rag = RAGService(
        organization=organization,
        clerk=clerk,
        knowledge=knowledge,
    )

    response = rag.invoke(quiestion=question, session_id=session_id)

    return response


@router.post('/train', status_code=200)
async def train(
    db: GetSharedDB,
    host_db: GetHostDB,
    host_name: GetHostName,
    knowledge_id: str,
):
    organization_repo = OrganizationRepository(db=db)
    knowledge_repo = KnowledgeRepository(db=host_db)
    clerk_repo = ClerkRepository(db=host_db)

    organization = await organization_repo.get_or_rise(
        by='host',
        value=host_name,
    )
    knowledge = await knowledge_repo.get_or_rise(
        by='_id',
        value=ObjectId(knowledge_id),
    )
    clerk = await clerk_repo.get_or_rise(
        by='_id',
        value=knowledge.clerk,
    )

    rag = RAGService(
        organization=organization,
        clerk=clerk,
        knowledge=knowledge,
    )

    await rag.train()


# class History(BaseModel):
#     type:
#     data:
# class ChatHistory(BaseModel):
#     id: ObjectIdField = Field(default=..., alias='_id')
#     session_id: str = Field(default=..., alias='SessionId')
#     history: History = Field(default=...)

#     model_config = ConfigDict(populate_by_name=True)


@router.get('/chat-history', status_code=200)
async def chat_history(  # type: ignore
    host_db: GetHostDB,
    knowledge_id: str,
    session_id: str,
):
    knowledge_repo = KnowledgeRepository(db=host_db)

    knowledge = await knowledge_repo.get_or_rise(
        by='_id',
        value=ObjectId(knowledge_id),
    )

    _filter = f'{str(knowledge.id)}:{session_id}'

    history = (
        await host_db['chat-history'].find({'SessionId': _filter}).to_list(30)
    )

    def parse(item):  # type: ignore
        history = json.loads(item['History'])  # type: ignore
        return {
            'id': str(item['_id']),  # type: ignore
            session_id: item['SessionId'],
            'type': history['type'],
            'content': history['data']['content'],
        }

    chat_history = [parse(item) for item in history]  # type: ignore

    response = {
        'knowledge': knowledge.model_dump(),
        'history': chat_history,
    }

    return response
