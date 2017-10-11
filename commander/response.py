from typing import List


class Response():
    def __init__(self, return_code: int, std_out: List[str], std_err: List[str]):
        self.return_code: int = return_code
        self.std_out: List[str] = std_out
        self.std_err: List[str] = std_err
