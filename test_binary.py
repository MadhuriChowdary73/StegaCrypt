from binary_utils import text_to_binary , binary_to_text
message="hello"
binary=text_to_binary(message)
decoded=binary_to_text(binary)
print("message:",message)
print("Binary:",binary)
print("Decoded:",decoded)