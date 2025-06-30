try:
    with open("output.txt", "r") as file:
        print("Reading file content:\n")
        line_number = 1
        for line in file:
            print(f"Line {line_number}: {line.strip()}")
            line_number += 1
except FileNotFoundError:
    print("Error: The file 'output.txt' does not exist.")
    
