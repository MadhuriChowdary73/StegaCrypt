def embed_bit(value:int,bit:int) -> int:
    value =value & 0b11111110

    if bit == 1:
        value=value | 0b00000001
    return value

