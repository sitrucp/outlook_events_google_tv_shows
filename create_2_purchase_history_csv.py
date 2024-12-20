import json
import csv

# Path to your JSON file
input_file = 'Purchase History.json'
# Path for the output CSV file
output_file = 'Purchase History.csv'

# Read the JSON data
with open(input_file, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Open a CSV file for writing
with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    # Write the header row
    writer.writerow(['documentType', 'title', 'purchaseTime'])

    # Iterate over each record in the JSON data
    for item in data:
        doc = item['purchaseHistory']['doc']
        purchaseTime = item['purchaseHistory'].get('purchaseTime', '')
        
        writer.writerow([doc['documentType'], doc['title'], purchaseTime])

print('CSV file has been created successfully.')
