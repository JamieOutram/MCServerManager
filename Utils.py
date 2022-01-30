from datetime import datetime as dt, timedelta


def seconds_till_time(hour, minute):
    now = dt.now()

    # Target time could be either today or tomorrow
    then = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if then <= now:
        then = then + timedelta(days=1)

    return (then-now).total_seconds(), then
