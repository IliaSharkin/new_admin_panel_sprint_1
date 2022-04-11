import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Film_work:
    title: str
    description: str
    creation_date: datetime
    certificate: str
    file_path: str
    rating: float
    type: str
    created_at: datetime
    updated_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Genre:
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Genre_film_work:
    film_work_id: str
    genre_id: str
    created_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Person:
    full_name: str
    birth_date: datetime
    created_at: datetime
    updated_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Person_film_work:
    film_work_id: str
    person_id: str
    role: str
    created_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)
