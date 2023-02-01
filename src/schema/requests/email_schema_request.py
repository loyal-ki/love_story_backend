from typing import Any, Dict, List
from pydantic import EmailStr, BaseModel


class EmailSchema(BaseModel):
    email: List[EmailStr]
    body: Dict[str, Any]
