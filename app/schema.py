from sqlalchemy import text

from app.database import get_engine


def create_tables():
    """Create all DataForge database tables."""

    engine = get_engine()

    with engine.begin() as connection:

        # Customers
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                region TEXT,
                signup_date DATE
            )
        """))

        # Products
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY,
                product_name TEXT NOT NULL,
                category TEXT,
                price REAL NOT NULL,
                stock_quantity INTEGER DEFAULT 0
            )
        """))

        # Orders
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY,
                customer_id INTEGER NOT NULL,
                order_date DATE,
                status TEXT,
                total_amount REAL,
                FOREIGN KEY (customer_id)
                    REFERENCES customers(customer_id)
            )
        """))

        # Order items
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS order_items (
                order_item_id INTEGER PRIMARY KEY,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                FOREIGN KEY (order_id)
                    REFERENCES orders(order_id),
                FOREIGN KEY (product_id)
                    REFERENCES products(product_id)
            )
        """))

        # Payments
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS payments (
                payment_id INTEGER PRIMARY KEY,
                order_id INTEGER NOT NULL,
                payment_date DATE,
                amount REAL,
                payment_method TEXT,
                payment_status TEXT,
                FOREIGN KEY (order_id)
                    REFERENCES orders(order_id)
            )
        """))

        # Employees
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS employees (
                employee_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                department TEXT,
                salary REAL,
                hire_date DATE
            )
        """))

        # Support tickets
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS support_tickets (
                ticket_id INTEGER PRIMARY KEY,
                customer_id INTEGER NOT NULL,
                issue_type TEXT,
                priority TEXT,
                status TEXT,
                created_at DATE,
                FOREIGN KEY (customer_id)
                    REFERENCES customers(customer_id)
            )
        """))

    print("All DataForge tables created successfully.")


if __name__ == "__main__":
    create_tables()