"""
binary_utils.py

Description:
Contains helper functions for converting
between text, integers and binary strings.

Author: MadhuriChowdary ,Kundan Sri Vyshnavi 
Project: StegaCrypt
"""


def text_to_binary(text: str) -> str:
    binary=""
    for ch in text :
        
        binary+=format(ord(ch),"08b")

    return binary 


def binary_to_text(binary:str)->str:
    text=""
    for i in range(0,len(binary),8):
        byte=binary[i:i+8]
        text+=chr(int(byte,2))

    return text

