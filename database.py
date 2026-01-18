from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus

password = quote_plus("Jatin@1999")
# Database connection URL
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{password}@localhost/book_db"

# SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# customized Session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models to inherit from
Base = declarative_base()

# Dependency function to be used in FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()