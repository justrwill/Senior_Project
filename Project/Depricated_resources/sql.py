import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('chinese_words.db')
cursor = conn.cursor()

# SQL script to create table and insert data, IN SOME FINAL VERSION OF THIS THESE ARE GOING TO BE CHARS probably
sql_script = '''
CREATE TABLE chinese_words (
    word TEXT,
    translation TEXT,
    pos TEXT , 
    definition TEXT ,
    pronunciation TEXT 
    
);

INSERT INTO chinese_words (word, translation, pos, definition, pronunciation)
VALUES ('我', 'I', 'noun' , 'First person singular pronoun in English, used to refer to oneself.','wŏ');
'''

# Execute the script
cursor.executescript(sql_script)

# Commit changes and close connection
conn.commit()
conn.close()

print("SQL script executed successfully.")
