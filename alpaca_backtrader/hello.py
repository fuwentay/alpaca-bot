import csv
import pandas as pd
from datetime import datetime, timedelta

# Parameters
start_date = datetime(2023, 1, 13)
end_date = datetime(2023, 1, 14)
time_delta = timedelta(minutes=15)  # Assuming you want data points every 15 minutes
impact_score_range = (50, 100)  # Example range of impact scores

# Generate datetime range
current_datetime = start_date
datetimes = []
while current_datetime <= end_date:
    datetimes.append(current_datetime)
    current_datetime += time_delta

# Generate impact scores (for demonstration, these are random)
import random
impact_scores = [random.randint(*impact_score_range) for _ in datetimes]

# Write to CSV
csv_file_path = 'impact2.csv'
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['datetime', 'impact_score'])  # Writing headers
    for dt, score in zip(datetimes, impact_scores):
        formatted_datetime = dt.strftime('%Y/%m/%d %H:%M:%S')
        writer.writerow([formatted_datetime, score])

print(f"CSV file '{csv_file_path}' has been created with {len(datetimes)} data points.")
