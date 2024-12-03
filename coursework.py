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
            data[i] = (data[i] and 0b11111110) | int(binary_message[message_idx])
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

def main(): 
    while True: #Starts an infinite loop for the main menu
        print("1. Encode a secret message") #Display option 1
        print("2. Decode a secret message") #Display option 2
        print("3. Exit") #Display option 3 
        choice = input("Enter your choice: ") 

        if choice == "1": #If the user chooses to input message 
            input_image = input("Enter the path to the input BMP image: ") #Input path for BMP image
            output_image = input("Enter the path to the output BMP image: ") #Output path for BMP image 
            message = input("Enter the message to hide: ") #Secret message to encode

            try: 
                header, data = read_bmp(input_image) #Read the bmp file and extract the header and data
                modified_data = encode_message(data, message) #Encode the secret message into the pixel data
                write_bmp(output_image, header, modified_data) #Saves the new data to a bmp file
                print("Message encoded and saved to", output_image) #Confirming encoding success
            except Exception as e: #Assigns error as "e"
                print("Error:", e) #Prints the type of error

        elif choice == "2": #User decides to decode the secret message
            input_image = input("Enter the path to the BMP image: ") #Enter the output path for the bmp image

            try:
                _, data = read_bmp(input_image) #Reads the bmp file and extracts the pixel dats with the message
                message = decode_message(data) #Decodes the message from the data 
                print("Decoded message:", message) #Prints the secret message
            except Exception as e: #Sets any errors as "e"
                print("Error:", e) #Displays the error message
        elif choice == "3": #User decides to exit the program
            print("Exiting the program.") #Alerts user
            break #Exists the program

        else: #If the user inputs anything other than "1" "2" "3"
            print("Invalid choice. Please try again.") #Notifies the user

if __name__ == "__main__": #Entry point of the script
    main() #Calls the main function to start the program

    