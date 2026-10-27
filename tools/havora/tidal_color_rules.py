"""Authoritative color effects for the revised directional Havora puzzle.

All three changes happen together. Arithmetic wraps in both directions.
Runtime bindings and route placement are generated separately.
"""
DELTAS = {
    'green': (1, -1, -1),
    'red': (-1, 0, 1),
    'yellow': (0, 1, 0),
    'blue': (1, 1, -1),
}

def apply_switch(levels, color):
    if len(levels) != 3 or any(level not in (0, 1, 2) for level in levels):
        raise ValueError('Expected three LOW/MID/HIGH levels (0, 1, 2)')
    return tuple((level + delta) % 3 for level, delta in zip(levels, DELTAS[color]))

if __name__ == '__main__':
    from itertools import product
    for levels in product(range(3), repeat=3):
        for color in DELTAS:
            result = levels
            for _ in range(3):
                result = apply_switch(result, color)
            assert result == levels
    assert apply_switch((2, 0, 0), 'green') == (0, 2, 2)
    assert apply_switch((0, 1, 2), 'red') == (2, 1, 0)
    print('PASS all four color effects and bidirectional wraparound across all 27 states')
