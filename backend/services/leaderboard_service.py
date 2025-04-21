#Imports
from datetime import datetime, timedelta
from sqlalchemy import func
from models import db
from models.user import User
from models.patient import Patient
from models.health_history import HealthHistory


#Leaderboard Utilities

def format_rank(i):
    """
    Returns a rank symbol (medal emoji for top 3, numeric otherwise).
    """
    medals = {0: "🥇", 1: "🥈", 2: "🥉"}
    return medals.get(i, str(i + 1))


def get_rank_class(i):
    """
    Returns a CSS class name for styling leaderboard rows.
    """
    classes = {0: "gold-row", 1: "silver-row", 2: "bronze-row"}
    return classes.get(i, "")


def get_timeframe_filter(timeframe):

    now = datetime.utcnow()
    if timeframe == "daily":
        return HealthHistory.recorded_at >= now - timedelta(days=1)
    elif timeframe == "weekly":
        return HealthHistory.recorded_at >= now - timedelta(weeks=1)
    elif timeframe == "monthly":
        return HealthHistory.recorded_at >= now - timedelta(days=30)
    else:
        return True  #No time constraint fallback


#Main Leaderboard Query Function

def fetch_leaderboard(metric_name, timeframe):

    #Health History Metrics Leaderboard
    timeframe_filter = get_timeframe_filter(timeframe)

    results = (
        db.session.query(User.username, func.sum(HealthHistory.value))
        .join(HealthHistory, User.patient_id == HealthHistory.patient_id)
        .join(Patient, User.patient_id == Patient.patient_id)
        .filter(Patient.show_on_leaderboard.is_(True))
        .filter(HealthHistory.metric_name == metric_name)
        .filter(timeframe_filter)
        .group_by(User.username)
        .order_by(func.sum(HealthHistory.value).desc())
        .limit(5)
        .all()
    )

    return [
        {
            "rank": format_rank(i),
            "name": row[0],
            "score": round(row[1] or 0, 2),
            "row_class": get_rank_class(i)
        }
        for i, row in enumerate(results)
    ]
