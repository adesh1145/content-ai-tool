from typing import List

def greet(names: List[str]) -> str:
    a: List[str]=["Adesh", "Yadav",1]
    print(a)
    return f"Hello {', '.join(names)}"

result = greet(['Emil', 'Linus'])
print(result)