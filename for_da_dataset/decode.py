def decode_row(row_str):
    """Decodes a row string into a list of integers."""
    row_str = row_str.strip('[],\n')  # Remove brackets, commas, and newline characters
    numbers = row_str.split(' , ')  # Split by comma and space
    decoded_numbers = []
    for num in numbers:
        if num and num.strip().isdigit():  # Check if the string is a valid integer
            decoded_numbers.append(int(num.strip()))  # Remove leading/trailing spaces and convert to int
    return decoded_numbers

# Read the entire content of "deduplicated_data_no_conversion.txt" into a string variable.
with open("deduplicated_data_no_conversion.txt", 'r') as file:
  file_content = file.read()

# Split the string by newline characters to create a list of strings
rows = file_content.split('\n')

# Decode each row and remove duplicates
decoded_data = []
unique_rows = set()

for row in rows:
    decoded_row = decode_row(row)
    if tuple(decoded_row) not in unique_rows:
        unique_rows.add(tuple(decoded_row))
        decoded_data.append(decoded_row)
        
print(in)

# Write the decoded and de-duplicated data to a new text file called "decoded_deduplicated_data.txt"
with open("decoded_deduplicated_data.txt", 'w') as file:
  for row in decoded_data:
    file.write(str(row) + '\n')

# Display the first 5 rows of the decoded, de-duplicated data
print(decoded_data[:5])