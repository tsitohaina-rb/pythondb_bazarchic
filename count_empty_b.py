import csv

# Path to your CSV file
file_path = "1 - PATRIZIA PEPE HONEY PROPOSTA AI26.csv"

empty_count = 0

with open(file_path, newline='', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    
    # Skip header if you have one
    header = next(reader, None)
    
    for row in reader:
        # Check if column B (index 1) exists and is empty
        if len(row) > 1 and row[1].strip() == "":
            empty_count += 1

print(f"Number of empty rows in column B: {empty_count}")
