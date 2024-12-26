from beanie import Document
from typing import List, Optional, Union
from pydantic import Field
from datetime import datetime, timezone
import uuid

# class Config(Document):
#     name: str
#     value: Union[bool, str]

#     class Settings:
#         name = "config"

class CommonModel(Document):
    # id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    is_active: bool = Field(default=True)
    # created_at: datetime = Field(default_factory=datetime.now)
    # updated_at: datetime = Field(default_factory=datetime.now)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        use_state_management = True
        state_management_update_strategy = "ALWAYS"

    def save(self, **kwargs):
        self.updated_at = datetime.now(timezone.utc)
        return super().save(**kwargs)

    class Config:
        from_attributes = True

