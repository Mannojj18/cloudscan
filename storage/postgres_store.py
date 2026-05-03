
import os
from sqlalchemy import create_engine, text

def save_scan(findings):
    url = os.getenv("DATABASE_URL")

    if not url:
        return

    engine = create_engine(url)

    with engine.begin() as conn:
        conn.execute(text('''
            CREATE TABLE IF NOT EXISTS scans(
                id SERIAL PRIMARY KEY,
                instance_id TEXT,
                monthly_cost FLOAT
            )
        '''))

        for item in findings:
            conn.execute(
                text('''
                    INSERT INTO scans(instance_id,monthly_cost)
                    VALUES (:id,:cost)
                '''),
                {
                    "id": item["instance_id"],
                    "cost": item["monthly_cost"]
                }
            )
