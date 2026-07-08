from lsb_utils import embed_bit

tests = [
    (120, 1),
    (121, 0),
    (255, 1),
    (255, 0),
    (0, 1),
    (0, 0),
]

for value, bit in tests:
    result = embed_bit(value, bit)
    print(f"embed_bit({value}, {bit}) -> {result}")