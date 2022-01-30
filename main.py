
import subprocess
import time
from datetime import datetime as dt
from datetime import timedelta
import shlex
from Utils import seconds_till_time
from server_process_management import ServerProcess

BACKUP_TIME = "21:08"
TIME_FORMAT = "%H:%M"
SERVER_DIR = "C:\\Users\\Owner\\Documents Offline\\C Projects\\MC_Server_GUI\\Test_Server"


def main():
    server = ServerProcess(SERVER_DIR, log_file="test.log")
    server.start()

    try:
        while 1:
            sleep_seconds, next_time = seconds_till_time(
                dt.strptime(BACKUP_TIME, TIME_FORMAT).hour,
                dt.strptime(BACKUP_TIME, TIME_FORMAT).minute
            )
            sleep_seconds = int(sleep_seconds) + 1
            print(f"Sleeping for {sleep_seconds} until {next_time}")
            time.sleep(sleep_seconds)
            print("Executing backup...")
            server.send_command("save-off")
            server.send_command("save-all")
            time.sleep(10)  # TODO: Actually backup here
            server.send_command("save-on")
    except KeyboardInterrupt:
        print("Keyboard interrupt detected, quitting...")
        server.stop()

    print("End")


if __name__ == "__main__":
    main()

