import secrets
from datetime import date, timedelta

from sqlalchemy import text

from app.database import get_engine


def secure_randint(low, high):
    """Generate a secure random integer within an inclusive range."""
    return low + secrets.randbelow(high - low + 1)


def secure_choice(options):
    """Securely select one item from a sequence."""
    return secrets.choice(options)


def secure_sample(population, k):
    """Securely sample k distinct items from a population."""
    if k < 0 or k > len(population):
        raise ValueError("Sample size is out of range.")

    selected_indices = set()
    while len(selected_indices) < k:
        selected_indices.add(secrets.randbelow(len(population)))

    return [population[index] for index in sorted(selected_indices)]


def random_date(start_date, end_date):
    """Generate a random date between two dates."""
    days = (end_date - start_date).days
    return start_date + timedelta(days=secrets.randbelow(days + 1))


def seed_database():
    engine = get_engine()

    with engine.begin() as connection:

        # -------------------------------------------------
        # 1. CUSTOMERS
        # -------------------------------------------------

        customers = [
            (
                1,
                "Arun Kumar",
                "arun@example.com",
                "Chennai",
                "2025-01-15",
            ),
            (
                2,
                "Priya Sharma",
                "priya@example.com",
                "Bangalore",
                "2025-02-20",
            ),
            (
                3,
                "Rahul Singh",
                "rahul@example.com",
                "Hyderabad",
                "2025-03-10",
            ),
            (
                4,
                "Sneha Raj",
                "sneha@example.com",
                "Chennai",
                "2025-04-05",
            ),
            (
                5,
                "Vikram Patel",
                "vikram@example.com",
                "Mumbai",
                "2025-05-12",
            ),
            (
                6,
                "Divya Kumar",
                "divya@example.com",
                "Bangalore",
                "2025-06-18",
            ),
            (
                7,
                "Karthik S",
                "karthik@example.com",
                "Coimbatore",
                "2025-07-22",
            ),
            (
                8,
                "Anjali Menon",
                "anjali@example.com",
                "Kochi",
                "2025-08-14",
            ),
            (
                9,
                "Manoj R",
                "manoj@example.com",
                "Chennai",
                "2025-09-03",
            ),
            (
                10,
                "Meena Devi",
                "meena@example.com",
                "Madurai",
                "2025-10-11",
            ),
        ]

        connection.execute(
            text("""
                INSERT OR IGNORE INTO customers
                (customer_id, name, email, region, signup_date)
                VALUES
                (:customer_id, :name, :email, :region, :signup_date)
            """),
            [
                {
                    "customer_id": row[0],
                    "name": row[1],
                    "email": row[2],
                    "region": row[3],
                    "signup_date": row[4],
                }
                for row in customers
            ],
        )

        # -------------------------------------------------
        # 2. PRODUCTS
        # -------------------------------------------------

        products = [
            (1, "Laptop Pro 14", "Electronics", 85000, 25),
            (2, "Wireless Mouse", "Accessories", 1200, 150),
            (3, "Mechanical Keyboard", "Accessories", 4500, 80),
            (4, "USB-C Hub", "Accessories", 2200, 100),
            (5, "27-inch Monitor", "Electronics", 24000, 40),
            (6, "Noise Cancelling Headphones", "Audio", 12000, 60),
            (7, "Bluetooth Speaker", "Audio", 6500, 75),
            (8, "Webcam HD", "Electronics", 3500, 90),
            (9, "Office Chair", "Furniture", 15000, 35),
            (10, "Standing Desk", "Furniture", 28000, 20),
        ]

        connection.execute(
            text("""
                INSERT OR IGNORE INTO products
                (product_id, product_name, category, price, stock_quantity)
                VALUES
                (:product_id, :product_name, :category, :price, :stock_quantity)
            """),
            [
                {
                    "product_id": row[0],
                    "product_name": row[1],
                    "category": row[2],
                    "price": row[3],
                    "stock_quantity": row[4],
                }
                for row in products
            ],
        )

        # -------------------------------------------------
        # 3. EMPLOYEES
        # -------------------------------------------------

        employees = [
            (1, "Amit", "Engineering", 85000, "2023-01-10"),
            (2, "Neha", "Engineering", 92000, "2022-08-15"),
            (3, "Ravi", "Sales", 65000, "2024-02-20"),
            (4, "Pooja", "Sales", 70000, "2023-11-05"),
            (5, "Sanjay", "HR", 60000, "2022-06-12"),
            (6, "Lakshmi", "Finance", 78000, "2021-09-18"),
            (7, "Arjun", "Engineering", 88000, "2024-01-25"),
            (8, "Nisha", "Support", 55000, "2024-03-10"),
        ]

        connection.execute(
            text("""
                INSERT OR IGNORE INTO employees
                (employee_id, name, department, salary, hire_date)
                VALUES
                (:employee_id, :name, :department, :salary, :hire_date)
            """),
            [
                {
                    "employee_id": row[0],
                    "name": row[1],
                    "department": row[2],
                    "salary": row[3],
                    "hire_date": row[4],
                }
                for row in employees
            ],
        )

        # -------------------------------------------------
        # 4. ORDERS
        # -------------------------------------------------

        order_rows = []

        for order_id in range(1, 51):
            customer_id = secure_randint(1, 10)
            order_date = random_date(
                date(2025, 1, 1),
                date(2025, 12, 31),
            )
            status = secure_choice(
                ["Completed", "Completed", "Completed", "Pending", "Cancelled"]
            )

            order_rows.append(
                {
                    "order_id": order_id,
                    "customer_id": customer_id,
                    "order_date": order_date.isoformat(),
                    "status": status,
                    "total_amount": 0,
                }
            )

        connection.execute(
            text("""
                INSERT OR IGNORE INTO orders
                (order_id, customer_id, order_date, status, total_amount)
                VALUES
                (:order_id, :customer_id, :order_date, :status, :total_amount)
            """),
            order_rows,
        )

        # -------------------------------------------------
        # 5. ORDER ITEMS
        # -------------------------------------------------

        order_item_rows = []
        item_id = 1

        for order in order_rows:

            number_of_items = secure_randint(1, 4)
            total = 0

            selected_products = secure_sample(
                products,
                number_of_items,
            )

            for product in selected_products:

                product_id = product[0]
                price = product[3]
                quantity = secure_randint(1, 3)

                total += price * quantity

                order_item_rows.append(
                    {
                        "order_item_id": item_id,
                        "order_id": order["order_id"],
                        "product_id": product_id,
                        "quantity": quantity,
                        "unit_price": price,
                    }
                )

                item_id += 1

            order["total_amount"] = total

        connection.execute(
            text("""
                INSERT OR IGNORE INTO order_items
                (order_item_id, order_id, product_id, quantity, unit_price)
                VALUES
                (:order_item_id, :order_id, :product_id,
                 :quantity, :unit_price)
            """),
            order_item_rows,
        )

        # Update order totals

        for order in order_rows:
            connection.execute(
                text("""
                    UPDATE orders
                    SET total_amount = :total_amount
                    WHERE order_id = :order_id
                """),
                order,
            )

        # -------------------------------------------------
        # 6. PAYMENTS
        # -------------------------------------------------

        payment_rows = []

        for order in order_rows:

            if order["status"] == "Cancelled":
                payment_status = "Refunded"

            elif order["status"] == "Pending":
                payment_status = "Pending"

            else:
                payment_status = "Paid"

            payment_rows.append(
                {
                    "payment_id": order["order_id"],
                    "order_id": order["order_id"],
                    "payment_date": order["order_date"],
                    "amount": order["total_amount"],
                    "payment_method": secure_choice(
                        ["UPI", "Credit Card", "Debit Card", "Net Banking"]
                    ),
                    "payment_status": payment_status,
                }
            )

        connection.execute(
            text("""
                INSERT OR IGNORE INTO payments
                (payment_id, order_id, payment_date, amount,
                 payment_method, payment_status)
                VALUES
                (:payment_id, :order_id, :payment_date, :amount,
                 :payment_method, :payment_status)
            """),
            payment_rows,
        )

        # -------------------------------------------------
        # 7. SUPPORT TICKETS
        # -------------------------------------------------

        ticket_rows = []

        for ticket_id in range(1, 31):

            ticket_rows.append(
                {
                    "ticket_id": ticket_id,
                    "customer_id": secure_randint(1, 10),
                    "issue_type": secure_choice(
                        [
                            "Payment Issue",
                            "Product Issue",
                            "Delivery Delay",
                            "Refund Request",
                            "Account Issue",
                        ]
                    ),
                    "priority": secure_choice(
                        ["Low", "Medium", "High"]
                    ),
                    "status": secure_choice(
                        ["Open", "In Progress", "Resolved"]
                    ),
                    "created_at": random_date(
                        date(2025, 1, 1),
                        date(2025, 12, 31),
                    ).isoformat(),
                }
            )

        connection.execute(
            text("""
                INSERT OR IGNORE INTO support_tickets
                (ticket_id, customer_id, issue_type, priority,
                 status, created_at)
                VALUES
                (:ticket_id, :customer_id, :issue_type, :priority,
                 :status, :created_at)
            """),
            ticket_rows,
        )

    print("DataForge database seeded successfully.")


if __name__ == "__main__":
    seed_database()