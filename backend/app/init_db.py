from .database import engine, Base
from .models import User, Movie, Theater, Booking

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    print("Tables created")