import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Filmwork:
    title: str
    description: str
    creation_date: datetime
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
class GenreFilmwork:
    film_work_id: str
    genre_id: str
    created_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Person:
    full_name: str
    created_at: datetime
    updated_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class PersonFilmwork:
    film_work_id: str
    person_id: str
    role: str
    created_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)
