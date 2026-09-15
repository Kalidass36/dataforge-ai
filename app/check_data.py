from sqlalchemy import text

from app.database import get_engine


def check_data():
    engine = get_engine()

    with engine.connect() as connection:

        tables = [
            "customers",
            "products",
            "employees",
            "orders",
            "order_items",
            "payments",
            "support_tickets",
        ]

        for table in tables:

            result = connection.execute(
                text(f"SELECT COUNT(*) FROM {table}")
            )

            count = result.scalar()

            print(f"{table}: {count} rows")


if __name__ == "__main__":
    check_data()