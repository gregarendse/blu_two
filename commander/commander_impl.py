import os
import subprocess

from commander import Commander, Response


class CommanderImpl(Commander):
    def __init__(self):
        super().__init__()

    def call(self, cmd: str) -> Response:
        completed = subprocess.run(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        return Response(
            completed.returncode,
            completed.stdout.decode('utf-8').split(os.linesep),
            completed.stderr.decode('utf-8').split(os.linesep)
        )
