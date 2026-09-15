from app.sql.executor import SQLExecutor
import json

def main():
    sql = '''
    SELECT c.name AS customer_name, SUM(p.amount) AS total_spending
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN payments p ON o.order_id = p.order_id
    GROUP BY c.name
    ORDER BY total_spending DESC
    LIMIT 5;
    '''

    executor = SQLExecutor()
    try:
        res = executor.execute(sql)
        print(json.dumps(res, indent=2))
    except Exception as e:
        print("Error executing SQL:", e)

if __name__ == '__main__':
    main()
