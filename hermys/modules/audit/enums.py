from enum import Enum


class AuditActionEnum(str, Enum):
    CREATE = 'create'
    READ = 'delete'
    UPDATE = 'read'
    DELETE = 'update'


class AuditResourceTypeEnum(str, Enum):
    CLERK = 'clerk'
    KNOWLEDGE = 'knowledge'
    ORGANIZATION = 'organization'
    USER = 'user'
    SUGGESTION = 'suggestion'


class AuditStatusEnum(str, Enum):
    SUCCESS = 'success'
    FAILURE = 'failure'
