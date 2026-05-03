
import os
from sqlalchemy import create_engine, text

def fetch_trend(instance_id):
    url = os.getenv("DATABASE_URL")

    if not url:
        return "No history"

    engine = create_engine(url)

    try:
        with engine.connect() as conn:
            rows = conn.execute(
                text('''
                SELECT monthly_cost
                FROM scans
                WHERE instance_id=:id
                ORDER BY id DESC
                LIMIT 2
                '''),
                {"id": instance_id}
            ).fetchall()

            if len(rows) < 2:
                return "Insufficient history"

            latest = rows[0][0]
            previous = rows[1][0]

            if latest > previous:
                return "Cost increasing"

            if latest < previous:
                return "Cost decreasing"

            return "Stable"

    except Exception:
        return "Trend unavailable"
