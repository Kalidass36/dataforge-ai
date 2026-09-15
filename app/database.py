from pathlib import Path

from sqlalchemy import create_engine, text


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database location
DATABASE_PATH = BASE_DIR / "data" / "dataforge.db"

# SQLite connection URL
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=False
)


def get_engine():
    """Return the SQLAlchemy database engine."""
    return engine


def initialize_database():
    """Create the database file and test the connection."""

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print(f"Database connection successful: {result.scalar()}")


if __name__ == "__main__":
    initialize_database()
    print(f"Database created at: {DATABASE_PATH}")