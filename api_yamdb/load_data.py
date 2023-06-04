import sqlite3
import csv
import os

db_path = '/db.sqlite3'
csv_folder = 'csv_folder/'
conn = sqlite3.connect(db_path)

for csv_file in os.listdir(csv_folder):
    if csv_file.endswith('.csv'):
        with open(os.path.join(csv_folder, csv_file), 'r') as f:
            reader = csv.reader(f)
            headers = next(reader)
            rows = [tuple(row) for row in reader]
        table_name = os.path.splitext(csv_file)[0]
        c = conn.cursor()
        c.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({", ".join(headers)})')
        c.executemany(f'INSERT INTO {table_name} VALUES ({", ".join(["?" for _ in headers])})', rows)
        conn.commit()
        c.close()
conn.close()
# для вызова написать python load_data.py в директории api_yamdb