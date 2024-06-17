import pandas as pd

# Define the base filename and file path for the CSV data
f_name = 'covid_19_data'
file_path = f"{f_name}.csv"

# Load the data from the specified CSV file using pandas
data = pd.read_csv(file_path)

# Define the size of each chunk for splitting the dataframe
chunk_size = 2000
# Calculate the number of chunks needed
num_chunks = len(data) // chunk_size + (1 if len(data) % chunk_size != 0 else 0)

# Process and save each chunk as a separate CSV file
for i in range(num_chunks):
    # Extract the subset of data for this chunk
    chunk = data.iloc[i*chunk_size:(i+1)*chunk_size]
    # Define the output filename for this chunk
    output_file = f"ShortFiles/{f_name}_part_{i+1}.csv"
    # Save the chunk to a CSV file without the index column
    chunk.to_csv(output_file, index=False)
    # Print confirmation that the file was saved successfully
    print(f"Saved {output_file}")