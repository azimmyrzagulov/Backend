from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Movie
from ..schemas import Movie as MovieSchema, MovieCreate
from ..auth import get_current_user

router = APIRouter()


def require_admin(current_user) -> None:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")

@router.get("/", response_model=list[MovieSchema])
def get_movies(
    skip: int = 0,
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    movies = db.query(Movie).offset(skip).limit(limit).all()
    return movies

@router.post("/", response_model=MovieSchema)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    require_admin(current_user)
    db_movie = Movie(**movie.model_dump())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


@router.put("/{movie_id}", response_model=MovieSchema)
def update_movie(
    movie_id: int,
    movie: MovieCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    require_admin(current_user)
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    for key, value in movie.model_dump().items():
        setattr(db_movie, key, value)

    db.commit()
    db.refresh(db_movie)
    return db_movie


@router.delete("/{movie_id}")
def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    require_admin(current_user)
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    db.delete(db_movie)
    db.commit()
    return {"message": "Movie deleted successfully"}
