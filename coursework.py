def read_bmp(filename): #The function reads a bmp file and extracts the header and pixel data
    with open(filename, "rb") as f: #Opens the file in binary read mode
        header = f.read(54)  #Reads thee 54 bytes header
        data = bytearray(f.read())  #Stores the remaining bytes into a changable bytearray
    return header, data #Return the header and data

def write_bmp(filename, header, data): #Writes a bmp image to file
    with open(filename, "wb") as f: #"wb" is to open the file in binary write mode
        f.write(header) #To write the unmodified BMP header 
        f.write(data)

def encode_message(data, message):
    binary_message = ""  # Stores the binary representation of the message as a single string
    for char in message: 
        ascii_value = ord(char)       # Convert char to ASCII value
        binary_char = f"{ascii_value:08b}"  # Convert ASCII value to binary "08" as in 8 bits
        binary_message += binary_char  # Adds the 8-bit binary representation of the character to the binary_message string
    binary_message += "00000000"  # Marks the end of the binary message

    message_idx = 0  # Initialize outside the loop

    for i in range(len(data)):
        if message_idx < len(binary_message):  # Ensure we don't exceed the message length
            data[i] = (data[i] & 0b11111110) | int(binary_message[message_idx])
            message_idx += 1
        else:
            break  # Exit loop when the entire message is encoded

    return data

def decode_message(data):
    binary_message = [] #Empty list to collect the binary bits
    for byte in data:
        binary_message.append(str(byte & 0b00000001))  # Extract LSB of each byte
        if len(binary_message) >= 8 and ''.join(binary_message[-8:]) == '00000000':  #Checks if the last 8 bits are 00000000, which indicates the end
            break

    chars = [chr(int(''.join(binary_message[i:i+8]), 2)) # Convert each 8-bit chunk from binary to a ASCII character.
             for i in range(0, len(binary_message) - 8, 8)] #Extracts 8 bits (one byte) at a time from the binary message.

    return ''.join(chars) #Combines all characters into a single string and returns it







