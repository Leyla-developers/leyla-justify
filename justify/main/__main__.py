from typing import List


class Justify:

    def  __init__(self) -> None:
        ...

    def eval(self, code):
        replaced_code = code.replace('`', '').replace('py', '') if code.startswith('```py') else code
        return eval(replaced_code)
