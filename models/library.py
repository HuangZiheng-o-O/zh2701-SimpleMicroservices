from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field


class LibraryBase(BaseModel):
    id: UUID = Field(
        ...,
        description="Library ID.",
        json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440000"},
    )
    code: str = Field(
        ...,
        description="Library code",
        json_schema_extra={"example": "BUT"},
    )
    name: str = Field(
        ...,
        description="Library name",
        json_schema_extra={"example": "Butler Library"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "code": "BUT",
                    "name": "Butler Library",
                }
            ]
        }
    }


 

class LibraryCreate(LibraryBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "11111111-1111-4111-8111-111111111111",
                    "code": "SEL",
                    "name": "Science & Engineering Library",
                }
            ]
        }
    }


class LibraryReplace(BaseModel):
    code: str = Field(
        ...,
        description="Library code",
        json_schema_extra={"example": "BUT"},
    )
    name: str = Field(
        ...,
        description="Library name",
        json_schema_extra={"example": "Butler Library"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": "SEL",
                    "name": "Science & Engineering Library",
                }
            ]
        }
    }


class LibraryUpdate(BaseModel):
    code: Optional[str] = Field(
        None,
        description="Library code",
        json_schema_extra={"example": "BUT"},
    )
    name: Optional[str] = Field(
        None,
        description="Library name",
        json_schema_extra={"example": "Butler Library"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"code": "AVY"},
                {"name": "Avery Architectural & Fine Arts Library"},
            ]
        }
    }



class LibraryRead(LibraryBase):
    id: UUID = Field(
        ...,
        description="Library ID.",
        json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440000"},
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "code": "BUT",
                    "name": "Butler Library",
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }


