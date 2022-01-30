
import subprocess
import time
from datetime import datetime as dt
from datetime import timedelta
import shlex

BACKUP_TIME = "18:08"
TIME_FORMAT = "%H:%M"


def start_process(stdout):
    print("Starting process...")
    pid = subprocess.Popen(
        shlex.split("java -Xmx1024M -Xms1024M -jar server.jar"),
        stdout=stdout,
        stdin=subprocess.PIPE
    )
    return pid


def send_command(command: str, pid):
    if not pid.poll():
        print(f"Sending {command}...")
        pid.communicate(input=f"{command}\r\n".encode('utf-8'))
    else:
        print("Process already terminated")


def seconds_till_time():
    now = dt.now()
    hour = dt.strptime(BACKUP_TIME, TIME_FORMAT).hour
    minute = dt.strptime(BACKUP_TIME, TIME_FORMAT).minute

    # Target time could be either today or tomorrow
    then = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if then <= now:
        then = then + timedelta(days=1)

    return (then-now).total_seconds(), then


def main():
    with open("test.log", "wb") as f:
        try:
            while 1:
                sleep_seconds, next_time = seconds_till_time()
                sleep_seconds = int(sleep_seconds) + 1
                print(f"Sleeping for {sleep_seconds} until {next_time}")
                time.sleep(sleep_seconds)
                print("Done Sleeping")
        except KeyboardInterrupt:
            print("Keyboard interrupt detected, quitting...")

    print("End")


if __name__ == "__main__":
    main()

