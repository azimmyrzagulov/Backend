from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..auth import get_current_user
from ..database import get_db
from ..models import Theater
from ..schemas import TheaterCreate, TheaterSchema, TheaterUpdate

router = APIRouter()


def require_admin(current_user) -> None:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")


@router.get("/", response_model=list[TheaterSchema])
def get_theaters(db: Session = Depends(get_db)):
    return db.query(Theater).all()


@router.post("/", response_model=TheaterSchema)
def create_theater(
    theater: TheaterCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    require_admin(current_user)
    db_theater = Theater(**theater.model_dump())
    db.add(db_theater)
    db.commit()
    db.refresh(db_theater)
    return db_theater


@router.put("/{theater_id}", response_model=TheaterSchema)
def update_theater(
    theater_id: int,
    theater: TheaterUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    require_admin(current_user)
    db_theater = db.query(Theater).filter(Theater.id == theater_id).first()
    if db_theater is None:
        raise HTTPException(status_code=404, detail="Theater not found")

    for key, value in theater.model_dump().items():
        setattr(db_theater, key, value)

    db.commit()
    db.refresh(db_theater)
    return db_theater


@router.delete("/{theater_id}")
def delete_theater(
    theater_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    require_admin(current_user)
    db_theater = db.query(Theater).filter(Theater.id == theater_id).first()
    if db_theater is None:
        raise HTTPException(status_code=404, detail="Theater not found")

    db.delete(db_theater)
    db.commit()
    return {"message": "Theater deleted successfully"}
