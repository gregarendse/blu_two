import os
from ctypes.wintypes import MAX_PATH

from commander import Commander, Response


class MockCommander(Commander):
    def __init__(self, return_code: int = None, std_out_source: str = None, std_err_source: str = None):
        super().__init__()
        self.std_out_source = std_out_source
        self.std_err_source = std_err_source
        self.return_code = return_code

    def call(self, cmd: str) -> Response:
        dir: str = os.path.join('F:\\workspace\\blu_two\\log', self.slugify(cmd))

        if len(dir) > MAX_PATH:
            dir = dir[0:MAX_PATH]

        with open(os.path.join(dir, 'std_out')) as file:
            std_out = file.read()

        with open(os.path.join(dir, 'std_err')) as file:
            std_err = file.read()

        with open(os.path.join(dir, 'return_code')) as file:
            return_code = int(file.readline())

        return Response(return_code, std_out.split('\n'), std_err.split('\n'))

