import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Render injects DATABASE_URL automatically once you connect a database.
# The fallback (after "or") is only used for local testing.
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:YOUR_PASSWORD@localhost:5432/skinalytix",
)

# Render's DATABASE_URL sometimes starts with "postgres://" — SQLAlchemy needs "postgresql://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()