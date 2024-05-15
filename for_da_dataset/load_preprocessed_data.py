import ast 

output_file = "preprocessed_scraped.txt" 

processed_data = []
with open(output_file, "r") as f:
    for line in f:
        parts = line.strip().split(",")
        # Ensure we have exactly two parts (input_ids and attention_mask)
        if len(parts) == 2: 
            input_ids_str, attention_mask_str = parts
            input_ids = ast.literal_eval(input_ids_str)
            attention_mask = ast.literal_eval(attention_mask_str)
            processed_data.append({"input_ids": input_ids, "attention_mask": attention_mask})
        else:
            print(f"Skipping invalid line: {line}")  # Optional: to log or handle invalid lines
