import pandas as pd

# Load the CSV files
df1 = pd.read_csv('Library.csv').rename(columns={'acquisitionTime': 'time'})
df2 = pd.read_csv('Purchase History.csv').rename(columns={'purchaseTime': 'time'})

# Combine the DataFrames, with Library.csv first to prioritize its records
combined_df = pd.concat([df1, df2])

# Filter for Tv Episode and Tv Movie document types
filtered_df = combined_df[combined_df['documentType'].isin(['Tv Episode', 'Movie'])]

# Deduplicate, keeping the first instance (prioritizing Library.csv due to the order in concat)
dedup_df = filtered_df.drop_duplicates(subset=['documentType', 'title'])

# Save the deduplicated DataFrame to a new CSV file
dedup_df.to_csv('combine_library_purch_hist.csv', index=False)

print('The combined, filtered, and deduplicated CSV file has been created.')
