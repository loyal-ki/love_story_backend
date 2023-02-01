from enum import Enum

# User status
class UserStatusEnum(int, Enum):
    online = 1
    offline = 2
    busy = 3
