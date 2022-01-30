import subprocess
import shlex
from datetime import datetime
import os


class ServerProcess:

    __pid = None
    __launch_seq: list = None
    __log = None
    __cwd = None

    def __init__(self,
                 cwd: str, launch_string: str = "java -Xmx1024M -Xms1024M -jar server.jar",
                 log_file: str = None):
        if not os.path.exists(cwd):
            raise OSError(cwd)

        self.__cwd = cwd

        self.__launch_seq = shlex.split(launch_string)

        if log_file:
            self.__log = open(log_file, "wb")

    def __del__(self):
        if self.__pid:
            self.stop(True)

        if self.__log:
            self.__log.close()

    def start(self):
        self.log("Starting server process...")
        self.__pid = subprocess.Popen(
            self.__launch_seq,
            stdout=None,
            stdin=subprocess.PIPE,
            cwd=self.__cwd
        )

    def send_command(self, command: str):
        if not self.__pid:
            print(f"ERROR: Must call start before sending a command.")
            return

        if not self.__pid.poll():
            self.log(f"Sending {command}...")
            self.__pid.communicate(input=f"{command}\r\n".encode('utf-8'))
        else:
            self.__pid.wait(timeout=1)  # Should return and update return code immediately
            self.log(f"ERROR: Process already terminated with code {self.__pid.returncode}, could not send command {command}")
            self.__pid = None

    def stop(self, force: bool = False):
        if not self.__pid:
            self.log("WARNING: No reference to running process to stop found")
            return

        if self.__pid.poll():
            self.log(f"ERROR: Process terminated prematurely with code {self.__pid.returncode}")
            __pid = None
            return

        if force:
            self.log(f"Terminating Process...")
            self.__pid.terminate()
            self.__pid.wait(timeout=5)
        else:
            self.send_command("stop")
            timeout = 30
            self.log(f"Waiting for server to close... (timeout {timeout}s)")
            self.__pid.wait(timeout=timeout)

        __pid = None

    def log(self, message: str):
        if self.__log:
            self.__log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]: {message}\r\n".encode("utf-8"))
