import jsons
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Container:
    contents: Dict[str, List[int]]

dictionary = {"key": [1, 2, 3]}
container = Container(contents=dictionary)
serialized = jsons.dump(container, verbose=True)
deserialized = jsons.load(serialized)
