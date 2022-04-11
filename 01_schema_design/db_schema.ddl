CREATE SCHEMA content;

SET search_path TO content,public;

CREATE TABLE film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    certificate TEXT,
    file_path TEXT,
    rating FLOAT,
    type TEXT not null,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

CREATE TABLE genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

 CREATE TABLE genre_film_work (
    id uuid PRIMARY KEY,
    film_work_id TEXT NOT NULL,
    genre_id TEXT NOT NULL,
    created_at timestamp with time zone
);
CREATE UNIQUE INDEX film_work_genre ON genre_film_work (film_work_id, genre_id);

CREATE TABLE person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    birth_date DATE,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

CREATE TABLE person_film_work (
    id uuid PRIMARY KEY,
    film_work_id TEXT NOT NULL,
    person_id TEXT NOT NULL,
    role TEXT NOT NULL,
    created_at timestamp with time zone
);
CREATE UNIQUE INDEX film_work_person_role ON person_film_work (film_work_id, person_id, role);
