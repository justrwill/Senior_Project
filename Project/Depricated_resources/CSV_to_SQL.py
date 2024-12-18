import sqlite3
import csv

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('chinese_words.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS chinese_words (
    chinese_char TEXT,
    english_word TEXT,
    definition TEXT
);
''')

# Read data from CSV and insert into database
with open('data.csv', 'r', newline='', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip header row if it exists
    
    for row in csvreader:
        chinese_char = row[0]
        english_word = row[1]
        definition = row[2]
        
        # Insert data into table
        cursor.execute('''
        INSERT INTO chinese_words (word, english_word, definition)
        VALUES (?, ?, ?);
        ''', (chinese_char, english_word, definition))

# Commit changes and close connection
conn.commit()
conn.close()

print("CSV data successfully imported into SQLite database.")
