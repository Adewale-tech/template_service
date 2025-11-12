import os
from sqlmodel import create_engine, SQLModel, Session

# --- Database Configuration ---
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./test.db")

# The connect_args are specific to SQLite.
# It's recommended to use check_same_thread=False only for single-threaded applications
# or when the application is managing thread safety. FastAPI with SQLModel/SQLAlchemy
# often requires this for SQLite.
engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

# --- Database Session Management ---
def get_session():
    """
    Dependency to get a database session.
    """
    with Session(engine) as session:
        yield session

async def create_db_and_tables():
    """
    Creates the database and all tables defined by SQLModel metadata.
    """
    # The following import is here to ensure that the models are registered with SQLModel
    # before the tables are created.
    from app import models  # noqa
    SQLModel.metadata.create_all(engine)

async def close_db_connection():
    """
    Closes the database connection engine.
    (Note: For some engines, this is not strictly necessary but is good practice)
    """
    # SQLAlchemy engines are designed to be long-lived and handle connection pooling.
    # Explicitly disposing of the engine is not always required on app shutdown,
    # but can be useful in certain deployment scenarios.
    engine.dispose()
