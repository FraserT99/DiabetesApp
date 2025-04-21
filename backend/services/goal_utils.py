import pandas as pd
from datetime import datetime, timedelta
import calendar
from pytz import timezone
from services.user_service import fetch_health_history, METRIC_GOAL_BEHAVIOR

UK_TZ = timezone("Europe/London")  #Local timezone for correct goal windows

def calculate_goal_progress(username, metric_name, goal_type, goal_value=None):
    df = fetch_health_history(username, metric_name)
    if df.empty:
        return None, None, [], [], 0

    df["Date"] = pd.to_datetime(df["Date"]).dt.tz_localize("UTC").dt.tz_convert(UK_TZ)

    today = datetime.now(UK_TZ).replace(hour=0, minute=0, second=0, microsecond=0)

    #Define time window based on goal_type
    if goal_type == "daily":
        start = today
        end = today + timedelta(days=1)
    elif goal_type == "weekly":
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=7)
    elif goal_type == "monthly":
        start = today.replace(day=1)
        last_day = calendar.monthrange(today.year, today.month)[1]
        end = today.replace(day=last_day, hour=23, minute=59, second=59)
    else:
        start = df["Date"].min()
        end = df["Date"].max()

    behavior = METRIC_GOAL_BEHAVIOR.get(metric_name, "cumulative")

    #Filter for goal window
    df_period = df[(df["Date"] >= start) & (df["Date"] <= end)].copy()
    if df_period.empty:
        return start, end, [], [], 0

    #Grouping
    if goal_type == "daily":
        df_period["Group"] = df_period["Date"].dt.floor("h")
    else:
        df_period["Group"] = df_period["Date"].dt.date

    #Behavior logic
    if behavior == "cumulative":
        df_grouped = df_period.groupby("Group")["Value"].sum().reset_index()
        df_grouped["Cumulative"] = df_grouped["Value"].cumsum()
        x_data = pd.to_datetime(df_grouped["Group"])
        y_data = df_grouped["Cumulative"]
        progress_value = y_data.iloc[-1]

    elif behavior == "average":
        df_grouped = df_period[["Group", "Value"]]
        x_data = pd.to_datetime(df_grouped["Group"])
        y_data = df_grouped["Value"]
        progress_value = y_data.mean()

    elif behavior == "change":
        #Use the first-ever recorded value as the baseline
        df_sorted = df.sort_values("Date")
        start_value = df_sorted.iloc[0]["Value"]
        current_value = df_period.iloc[-1]["Value"]

        required_change = abs(goal_value - start_value)
        actual_change = abs(current_value - start_value)

        direction_correct = (
            (start_value > goal_value and current_value < start_value) or
            (start_value < goal_value and current_value > start_value)
        )

        if not direction_correct:
            progress_value = 0
        elif required_change == 0:
            progress_value = 100
        else:
            progress_value = min(100, round((actual_change / required_change) * 100, 1))

        x_data = df_period["Date"]
        y_data = df_period["Value"]

    else:
        df_grouped = df_period.groupby("Group")["Value"].sum().reset_index()
        df_grouped["Cumulative"] = df_grouped["Value"].cumsum()
        x_data = pd.to_datetime(df_grouped["Group"])
        y_data = df_grouped["Cumulative"]
        progress_value = y_data.iloc[-1]

    return start, end, x_data, y_data, round(progress_value, 2)
