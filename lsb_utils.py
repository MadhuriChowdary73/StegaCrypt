def embed_bit(value:int,bit:int) -> int:
    value =value & 0b11111110

    if bit == 1:
        value=value | 0b00000001
    return value

def extract_bit(value:int) -> int:
     """
    Extract the least significant bit.

    Args:
        value (int): Pixel value (0–255)

    Returns:
        int: Hidden bit (0 or 1)
    """
     
     return value & 0b00000001

