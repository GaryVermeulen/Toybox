# testDictionary.py
#
# Dictionary fun (Oxford English Dictionary from 1968)
#

import sys

filePath = '/home/gary/tmp/oed_2/oed_1.txt'

def readFile():

    lineCount = 1

    try:
        with open(filePath, 'r', encoding='latin-1') as file:
            for line in file:
                # Each 'line' variable will contain one line from the file,
                # including the newline character at the end.
                # You can process or print the line here.
                print(f'>{line.strip()}<')  # .strip() removes leading/trailing whitespace, including the newline
                lineCount += 1

                if lineCount >= 100:
                    sys.exit("Limit reached.")
                    
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return


if __name__ == "__main__":


    readFile()
