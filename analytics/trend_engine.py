import os
from sqlalchemy import create_engine, text

# Create engine once (global)
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL) if DATABASE_URL else None


def fetch_trend(instance_id):
    if not engine:
        return "No history"

    try:
        with engine.connect() as conn:
            rows = conn.execute(
                text("""
                SELECT monthly_cost
                FROM scans
                WHERE instance_id = :id
                ORDER BY id DESC
                LIMIT 2
                """),
                {"id": instance_id}
            ).fetchall()

        if len(rows) < 2:
            return "Insufficient history"

        latest = rows[0][0]
        previous = rows[1][0]

        # Avoid divide by zero
        if previous == 0:
            return "Stable"

        change_percent = ((latest - previous) / previous) * 100

        # --- Industry-style classification ---
        if change_percent > 10:
            return f"Increasing (+{round(change_percent, 2)}%)"
        elif change_percent < -10:
            return f"Decreasing ({round(change_percent, 2)}%)"
        else:
            return f"Stable ({round(change_percent, 2)}%)"

    except Exception as e:
        return f"Trend unavailable ({str(e)})"