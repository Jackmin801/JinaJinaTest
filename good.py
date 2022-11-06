from typing import Dict, Optional

class Meow:
    def __init__(self, arg: Optional[Dict[str, str]] = None) -> None:
        if arg is None:
            arg = {}
        self.arg = arg

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(arg={self.arg})"

a = Meow()
b = Meow()

a.arg['Dog'] = "Woof"
print(a)
print(b)

b.arg['Pig'] = "Oink"
print(a)
print(b)