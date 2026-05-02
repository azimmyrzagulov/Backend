#!/usr/bin/env python
from datetime import datetime

from app.database import SessionLocal
from app.models import Movie


MOVIES = [
    {
        "title": "Zootopia 2",
        "description": "Animated buddy-cop adventure in the bustling city of Zootopia.",
        "genre": "Animation | Family | Adventure",
        "duration": 107,
        "release_date": datetime(2025, 11, 26),
        "poster_url": "/posters/zootopia-2.svg",
    },
    {
        "title": "Avatar: Fire and Ash",
        "description": "An epic science-fiction journey back to Pandora.",
        "genre": "Science Fiction | Adventure | Fantasy",
        "duration": 198,
        "release_date": datetime(2025, 12, 19),
        "poster_url": "/posters/avatar-fire-and-ash.svg",
    },
    {
        "title": "Sinners",
        "description": "Brothers return home and face a sinister force waiting for them.",
        "genre": "Horror | Thriller",
        "duration": 138,
        "release_date": datetime(2025, 4, 18),
        "poster_url": "/posters/sinners.svg",
    },
    {
        "title": "Dune: Part Two",
        "description": "Paul Atreides joins the Fremen to shape the fate of Arrakis.",
        "genre": "Science Fiction | Adventure",
        "duration": 167,
        "release_date": datetime(2024, 3, 1),
        "poster_url": "/posters/dune-part-two.svg",
    },
    {
        "title": "Inside Out 2",
        "description": "Riley's mind gets even more crowded as new emotions arrive.",
        "genre": "Animation | Family | Comedy",
        "duration": 96,
        "release_date": datetime(2024, 6, 14),
        "poster_url": "/posters/inside-out-2.svg",
    },
    {
        "title": "The Wild Robot",
        "description": "A service robot learns to survive and care for a wild island.",
        "genre": "Animation | Science Fiction | Family",
        "duration": 102,
        "release_date": datetime(2024, 9, 27),
        "poster_url": "/posters/the-wild-robot.svg",
    },
    {
        "title": "Furiosa: A Mad Max Saga",
        "description": "A relentless survival story set across the wasteland.",
        "genre": "Action | Science Fiction | Adventure",
        "duration": 148,
        "release_date": datetime(2024, 5, 24),
        "poster_url": "/posters/furiosa-a-mad-max-saga.svg",
    },
    {
        "title": "Spider-Man: Across the Spider-Verse",
        "description": "Miles Morales leaps across dimensions with a new team of heroes.",
        "genre": "Animation | Action | Adventure",
        "duration": 140,
        "release_date": datetime(2023, 6, 2),
        "poster_url": "/posters/spider-man-across-the-spider-verse.svg",
    },
    {
        "title": "Oppenheimer",
        "description": "A historical drama about the making of the atomic bomb.",
        "genre": "Drama | History | Thriller",
        "duration": 180,
        "release_date": datetime(2023, 7, 21),
        "poster_url": "/posters/oppenheimer.svg",
    },
    {
        "title": "Interstellar",
        "description": "Explorers travel beyond Earth in search of humanity's future.",
        "genre": "Science Fiction | Drama | Adventure",
        "duration": 169,
        "release_date": datetime(2014, 11, 7),
        "poster_url": "/posters/interstellar.svg",
    },
    {
        "title": "The Batman",
        "description": "Batman investigates corruption and a serial killer in Gotham.",
        "genre": "Action | Crime | Mystery",
        "duration": 176,
        "release_date": datetime(2022, 3, 4),
        "poster_url": "/posters/the-batman.svg",
    },
    {
        "title": "Top Gun: Maverick",
        "description": "Maverick trains a new generation of pilots for a dangerous mission.",
        "genre": "Action | Drama",
        "duration": 131,
        "release_date": datetime(2022, 5, 27),
        "poster_url": "/posters/top-gun-maverick.svg",
    },
    {
        "title": "Barbie",
        "description": "Barbie leaves Barbieland and discovers the real world.",
        "genre": "Comedy | Adventure | Fantasy",
        "duration": 114,
        "release_date": datetime(2023, 7, 21),
        "poster_url": "/posters/barbie.svg",
    },
    {
        "title": "Wonka",
        "description": "A whimsical origin story for the world's most inventive chocolatier.",
        "genre": "Family | Fantasy | Musical",
        "duration": 116,
        "release_date": datetime(2023, 12, 15),
        "poster_url": "/posters/wonka.svg",
    },
    {
        "title": "Mission: Impossible - Dead Reckoning",
        "description": "Ethan Hunt races to stop a dangerous AI threat.",
        "genre": "Action | Thriller | Adventure",
        "duration": 163,
        "release_date": datetime(2023, 7, 12),
        "poster_url": "/posters/mission-impossible-dead-reckoning.svg",
    },
]


def upsert_movies() -> None:
    db = SessionLocal()
    created = 0
    updated = 0

    try:
        for payload in MOVIES:
            movie = db.query(Movie).filter(Movie.title == payload["title"]).first()

            if movie is None:
                db.add(Movie(**payload))
                created += 1
                continue

            for key, value in payload.items():
                setattr(movie, key, value)
            updated += 1

        db.commit()

        all_movies = db.query(Movie).order_by(Movie.title.asc()).all()
        print("Movies synced successfully.")
        print(f"Created: {created}")
        print(f"Updated: {updated}")
        print(f"Total in database: {len(all_movies)}")
        for movie in all_movies:
            print(f"  - {movie.title} -> {movie.poster_url}")
    finally:
        db.close()


if __name__ == "__main__":
    upsert_movies()
