from enum import Enum


class UserRoleEnum(str, Enum):
    GOD = 'god'
    ADMIN = 'admin'
    USER = 'user'
