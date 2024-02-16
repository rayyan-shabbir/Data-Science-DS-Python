f = open("task1.bin", "r")
hex_str = f.readline()[2:]
byte_array = bytes.fromhex(hex_str)
ascii_str = byte_array.decode()
print("ASCII : " + ascii_str)

# print(f.read())

# hex_str = "ox68656c6f"[2:]
