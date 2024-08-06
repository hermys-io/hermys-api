import json

from bson import ObjectId
from fastapi import APIRouter

from hermys.common.host_name_dependencies import GetHostName
from hermys.db.host_db import GetHostDB
from hermys.db.shared_db import GetSharedDB
from hermys.integrations.b2.dependencies import GetB2Integration
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


@router.get('/clerk', status_code=200)
async def get_clerk(
    clerk_slug: str,
    host_db: GetHostDB,
):
    clerk_repo = ClerkRepository(db=host_db)

    clerk = await clerk_repo.get_or_rise(by='slug', value=clerk_slug)

    return clerk.model_dump()


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

    if len(history) == 0:  # type: ignore
        welcome_message = await host_db['chat-history'].insert_one(
            {
                'SessionId': f'{str(knowledge.id)}:{session_id}',
                'History': json.dumps(
                    {
                        'type': 'ai',
                        'data': {'content': knowledge.welcome_message},
                    }
                ),
            }
        )
        history.append(welcome_message)

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


@router.get('/get-signed-file')
async def get_signed_file(
    b2_integration: GetB2Integration,
    filename: str,
    _host_db: GetHostDB,
    valid_duration_in_seconds: int = 3600,
):
    result = b2_integration.get_file(
        filename=filename,
        valid_duration_in_seconds=valid_duration_in_seconds,
    )
    return result
