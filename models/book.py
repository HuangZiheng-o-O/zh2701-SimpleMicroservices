from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field


class BookBase(BaseModel):
    id: UUID = Field(
        ...,
        description="Book ID.",
        json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440000"},
    )
    title: str = Field(
        ...,
        description="Book title",
        json_schema_extra={"example": "Trumpbook"},
    )
    author: Optional[str] = Field(
        None,
        description="Book author",
        json_schema_extra={"example": "Trump"},
    )
    price: float = Field(
        ...,
        description="Non-negative price",
        ge=0,
        json_schema_extra={"example": 33.33},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "title": "Trumpbook",
                    "author": "Trump",
                    "price": 33.33,
                }
            ]
        }
    }


class BookCreate(BookBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "5b526ffa-7b06-41fc-a24e-e87520970da2",
                    "title": "Bidenbook",
                    "author": "Biden",
                    "price": 20.00,
                }
            ]
        }
    }


class BookReplace(BaseModel):
    title: str = Field(
        ...,
        description="Book title",
        json_schema_extra={"example": "Trumpbook"},
    )
    author: Optional[str] = Field(
        None,
        description="Book author",
        json_schema_extra={"example": "Trump"},
    )
    price: float = Field(
        ...,
        description="Non-negative price",
        ge=0,
        json_schema_extra={"example": 33.33},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Bidenbook",
                    "author": "Biden",
                    "price": 67.44,
                }
            ]
        }
    }


class BookUpdate(BaseModel):
    title: Optional[str] = Field(
        None,
        description="Book title",
        json_schema_extra={"example": "Trumpbook"},
    )
    author: Optional[str] = Field(
        None,
        description="Book author",
        json_schema_extra={"example": "Trump"},
    )
    price: Optional[float] = Field(
        None,
        description="Non-negative price",
        ge=0,
        json_schema_extra={"example": 33.33},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"title": "Trumpbook: Revised Edition"},
                {"price": 14.99},
                {"author": "Trump"},
            ]
        }
    }


class BookRead(BookBase):
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
                    "title": "Trumpbook",
                    "author": "Trump",
                    "price": 33.33,
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }