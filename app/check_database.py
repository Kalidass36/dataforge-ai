from sqlalchemy import text

from app.database import get_engine


def check_tables():
    engine = get_engine()

    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                ORDER BY name
            """)
        )

        tables = result.fetchall()

        print("DataForge tables:")
        for table in tables:
            print(f"- {table[0]}")


if __name__ == "__main__":
    check_tables()