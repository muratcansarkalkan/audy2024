import struct

def int_to_uint16(value):
    """Convert an integer to UINT16 and return as a hexadecimal string."""
    value = int(value)
    if not (0 <= value <= 65535):
        raise ValueError("Value out of range for UINT16")
    uint16_bytes = struct.pack('H', value)
    return uint16_bytes.hex()

def int_to_uint8(value):
    """Convert an integer to UINT8 and return as a hexadecimal string."""
    if not (0 <= value <= 255):
        raise ValueError("Value out of range for UINT8")
    uint8_bytes = struct.pack('B', value)
    return uint8_bytes.hex()

# Example usage
value1 = "17354"
uint16_hex = int_to_uint16(value1)
value2 = 18
uint8_hex = int_to_uint8(value2)

print(f"Integer: {value1}")
print(f"UINT16 (hex): {uint16_hex}")
print(f"Integer: {value2}")
print(f"UINT8 (hex): {uint8_hex}")