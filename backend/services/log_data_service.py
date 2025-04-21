#Imports
from dash import html
from models.user import User
from models.health_history import HealthHistory
from services.user_service import METRIC_UNITS  #Dictionary mapping metric names to their units
from pytz import timezone, UTC  #⏰ For timezone conversions
from datetime import datetime, timedelta

#UK local timezone (handles DST automatically)
UK_TZ = timezone("Europe/London")


#Metric History Fetching

def fetch_metric_history(patient_id, metric_name):

    #Query the 5 most recent entries for this metric
    history_records = (
        HealthHistory.query
        .filter_by(patient_id=patient_id, metric_name=metric_name)
        .order_by(HealthHistory.recorded_at.desc())
        .limit(5)
        .all()
    )

    #Format display name
    metric_display_name = metric_name.replace("_", " ").title()

    #Get unit for this metric (if any)
    unit = METRIC_UNITS.get(metric_name, "")

    #No logs found → return placeholder message
    if not history_records:
        return html.Div([
            html.H5(f"Last 5 Logs - {metric_display_name}", className="metric-history-title"),
            html.P("No records available.", className="no-history-message")
        ], className="metric-history-container")

    #Generate visual log entries with UK-local timestamps
    return html.Div([
        html.H5(f"Last 5 Logs - {metric_display_name}", className="metric-history-title"),
        *[
            html.Div([
                html.Span(
                    #Convert UTC to local time and format
                    record.recorded_at.replace(tzinfo=UTC).astimezone(UK_TZ).strftime('%Y-%m-%d %H:%M'),
                    className="history-timestamp"
                ),
                html.Span(
                    f" → {round(record.value, 2)} {unit}",
                    className="history-value"
                ),
            ], className="history-entry")
            for record in history_records
        ]
    ], className="metric-history-container")

from pytz import UTC, timezone
UK_TZ = timezone("Europe/London")

def get_consecutive_log_streak(username):
    from datetime import timedelta

    user = User.query.filter_by(username=username).first()
    if not user or not user.patient:
        return 0

    logs = (
        HealthHistory.query
        .filter_by(patient_id=user.patient.patient_id)
        .with_entities(HealthHistory.recorded_at)
        .order_by(HealthHistory.recorded_at.desc())
        .all()
    )

    if not logs:
        print(f"[DEBUG] No logs found for {username}")
        return 0

    #Convert all timestamps to UK local dates
    log_dates = sorted({
        log.recorded_at.replace(tzinfo=UTC).astimezone(UK_TZ).date()
        for log in logs
    }, reverse=True)

    print(f"[DEBUG] All log dates for {username}: {log_dates}")

    streak = 0
    today = datetime.now(UK_TZ).date()

    for i, log_date in enumerate(log_dates):
        expected_date = today - timedelta(days=i)
        print(f"[DEBUG] Day {i}: log_date = {log_date}, expected = {expected_date}")

        if log_date == expected_date:
            streak += 1
        else:
            break

    print(f"[DEBUG] Final streak for {username}: {streak} days")
    return streak

from services.user_service import METRIC_LABELS, METRIC_UNITS, METRIC_GOAL_BEHAVIOR

def fetch_metric_summary(username, period="day"):
    user = User.query.filter_by(username=username).first()
    if not user or not user.patient:
        print(f"[DEBUG] User not found: {username}")
        return {}

    patient_id = user.patient.patient_id
    now = datetime.now(UK_TZ)

    #Define start and end of the selected period
    if period == "day":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    elif period == "week":
        start = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=6, hours=23, minutes=59, seconds=59)
    elif period == "month":
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        next_month = (now.replace(day=28) + timedelta(days=4)).replace(day=1)
        end = next_month - timedelta(microseconds=1)
    else:
        print(f"[DEBUG] Invalid period passed: {period}")
        return {}

    start_utc = start.astimezone(UTC)
    end_utc = end.astimezone(UTC)

    print(f"[DEBUG] Summary range ({period}): {start_utc} → {end_utc}")

    results = {}

    for metric, label in METRIC_LABELS.items():
        logs = (
            HealthHistory.query
            .filter_by(patient_id=patient_id, metric_name=metric)
            .filter(HealthHistory.recorded_at >= start_utc, HealthHistory.recorded_at <= end_utc)
            .order_by(HealthHistory.recorded_at.asc())
            .all()
        )

        print(f"[DEBUG] {metric}: {len(logs)} logs found in range")

        if not logs:
            continue

        behavior = METRIC_GOAL_BEHAVIOR.get(metric, "latest")
        values = [log.value for log in logs]

        if behavior == "cumulative":
            summary = round(sum(values), 2)
        elif behavior == "average":
            summary = round(sum(values) / len(values), 2)
        elif behavior == "change":
            summary = round(values[-1] - values[0], 2)
        else:
            summary = round(values[-1], 2)

        print(f"[DEBUG] → {behavior.title()} {label}: {summary} {METRIC_UNITS.get(metric, '')}")

        results[metric] = {
            "label": label,
            "value": summary,
            "unit": METRIC_UNITS.get(metric, "")
        }

    return results
