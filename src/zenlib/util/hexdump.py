from zenlib.util.colorize import colorize as c_

HEX_COLORS = {
    0: {"dim": True},  # Make null bytes dim
    32: {"dim": True},  # Make space dim
}

# Make punctuation and special characters red
for i in range(33, 48):  # Special characters
    HEX_COLORS[i] = {"color": "red", "bold": True}
for i in range(58, 65):  # Special characters
    HEX_COLORS[i] = {"color": "red", "bold": True}
for i in range(91, 97):  # Special characters
    HEX_COLORS[i] = {"color": "red", "bold": True}
for i in range(123, 127):  # Special characters
    HEX_COLORS[i] = {"color": "red", "bold": True}

# Make ASCII numbers green and bold
for i in range(48, 57):  # decimal numbers
    HEX_COLORS[i] = {"color": "green", "bold": True}

# Make ASCII letters blue and bold
for i in range(65, 91):  # Uppercase A-Z
    HEX_COLORS[i] = {"color": "blue", "bold": True}
for i in range(97, 123):  # Lowercase a-z
    HEX_COLORS[i] = {"color": "blue", "bold": True}

# Make extended ASCII characters yellow and bold
for i in range(128, 256):  # Extended ASCII
    HEX_COLORS[i] = {"color": "yellow", "bold": True}

# Make control characters magenta
for i in range(1, 32):  # Control characters
    HEX_COLORS[i] = {"color": "magenta"}


def get_hex_color(byte: int) -> str:
    """Returns the colorized representation of a byte."""
    if byte in HEX_COLORS:
        color_data = HEX_COLORS[byte]
        return c_(f"{byte:02x}", **color_data)
    return c_(f"{byte:02x}", bold=True)


def hexdump(data: bytes, length: int = 16, binary=False) -> str:
    """
    Returns a formatted hex dump of the given binary data.
    If `binary` is True, it will return a binary dump instead of hex.

    Args:
        data (bytes): The binary data to be dumped.
        length (int): The number of bytes per line in the dump.

    Returns:
        str: A formatted hex dump of the binary data.
    """
    result = []
    data_len =  length * 3 if not binary else length * 9
    for i in range(0, len(data), length):
        chunk = data[i : i + length]
        hex_part = " ".join(f"{get_hex_color(byte)}" for byte in chunk) if not binary else " ".join(f"{byte:08b}" for byte in chunk)
        hex_part = hex_part + " " * (data_len - (len(chunk) * (3 if not binary else 9)))
        ascii_part = "".join((c_(chr(byte), "green") if 32 <= byte < 127 else ".") for byte in chunk)
        result.append(f"{i:08x}:  {hex_part:<{data_len}} {ascii_part}")
    return "\n".join(result)
