from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from app.core.config import settings

# If using Supabase Pooler (Transaction/Session mode), it's recommended to use NullPool
# to let Supabase manage the connection pooling and avoid client-side state issues.
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=NullPool,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
