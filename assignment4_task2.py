text = input("Enter text to write to the file: ")
try:
    with open("output.txt", "w") as file:
        file.write(text + "\n")
    print("Data successfully written to output.txt.")
except Exception as e:
    print("Error writing to file:", e)

more_text = input("\nEnter additional text to append: ")
try:
    with open("output.txt", "a") as file:
        file.write(more_text + "\n")
    print("Data successfully appended.")
except Exception as e:
    print("Error appending to file:", e)

print("\nFinal content of output.txt:")
try:
    with open("output.txt", "r") as file:
        for line in file:
            print(line.strip())
except FileNotFoundError:
    print("Error: output.txt not found.")
except Exception as e:
    print("Error reading the file:", e)

