import json
import csv

# Path to your JSON file
input_file = 'Library.json'
# Path for the output CSV file
output_file = 'Library.csv'

# Read the JSON data
with open(input_file, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Open a CSV file for writing
with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    # Write the header row
    writer.writerow(['documentType', 'title', 'acquisitionTime'])

    # Iterate over each record in the JSON data
    for item in data:
        doc = item['libraryDoc']['doc']
        # Check if 'acquisitionTime' exists, else use a default value or leave it empty
        acquisitionTime = item['libraryDoc'].get('acquisitionTime', '')
        
        writer.writerow([doc['documentType'], doc['title'], acquisitionTime])

print('CSV file has been created successfully.')
