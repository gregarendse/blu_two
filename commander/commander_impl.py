import logging
import os
import re
import subprocess
import time
from ctypes.wintypes import MAX_PATH

from commander import Commander, Response

logger = logging.getLogger(__name__)


class CommanderImpl(Commander):
    def __init__(self):
        super().__init__()

    def call(self, cmd: str) -> Response:
        logger.info('Executing command, command: %s', cmd)
        start: int = time.time()

        completed = subprocess.run(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        end: int = time.time()
        duration: int = end - start

        response: Response = Response(
            completed.returncode,
            completed.stdout.decode('utf-8').split(os.linesep),
            completed.stderr.decode('utf-8').split(os.linesep)
        )

        self.log_output(cmd=cmd, response=response)
        logger.info('Finished, execution_time: %d, return_code: %d', duration, response.return_code)

        return response

    def log_output(self, cmd: str, response: Response) -> None:
        dir: str = os.path.join('F:\\workspace\\blu_two\\log', self.slugify(cmd))

        if len(dir) > MAX_PATH:
            dir = dir[0:MAX_PATH]

        os.makedirs(dir, exist_ok=True)

        with open('{}/return_code'.format(dir), 'w') as file:
            file.write(str(response.return_code))

        with open('{}/std_out'.format(dir), 'w') as file:
            for line in response.std_out:
                file.write("{line}\n".format(line=line))

        with open('{}/std_err'.format(dir), 'w') as file:
            for line in response.std_err:
                file.write("{line}\n".format(line=line))
