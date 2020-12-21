from typing import Dict, TypeVar, Set

T = TypeVar('T')
U = TypeVar('U')


def reduce_possibilities(possibility_map: Dict[T, Set[U]]) -> Dict[T, U]:
    # Let's make a copy in case the caller wanted to keep their map
    possibility_map = possibility_map.copy()
    result: Dict[T, U] = {}

    something_changed = True
    while something_changed:
        something_changed = False
        for key, possibilities in possibility_map.copy().items():
            if len(possibilities) == 1:
                something_changed = True
                known_item = list(possibilities)[0]
                result[key] = known_item

                del possibility_map[key]

                for values in possibility_map.values():
                    if known_item in values:
                        values.remove(known_item)

    if len(possibility_map) > 0:
        raise ValueError(f"Couldn't reduce all possibilities")

    return result
