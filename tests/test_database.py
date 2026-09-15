from pathlib import Path

from app.database import DATABASE_PATH, get_engine


def test_database_path_and_engine() -> None:
    assert DATABASE_PATH.parent.exists()
    assert get_engine() is not None
    assert isinstance(DATABASE_PATH, Path)
