#Justin Williams 

import os
import sqlite3

class retrieval:
    #Current Needs : [Need to build database/csvs , to build parse function that handles compounds/sentences]
    # Future Needs: [need to generalize dictionary/sql queries , package everything together, add front end]                  
    

    def __init__(self, lang):
        self.lang = lang ##idk if you need this or not, but
        self.setDB(lang)

    def getDefinition(self, word):
        res = self.cursor.execute('SELECT definition FROM chinese_words WHERE word = ?', (word,)) #Need to change chinese_words to find a way to change the table to Lang
        definition = res.fetchone()
        return definition[0] if definition else None

    def getPos(self, word):
        res = self.cursor.execute('SELECT pos FROM chinese_words WHERE word = ?', (word,))
        pos = res.fetchone()
        return pos[0] if pos else None

    def getTranslation(self, word):
        res = self.cursor.execute('SELECT translation FROM chinese_words WHERE word = ?', (word,))
        translations = res.fetchall()
        return [translation[0] for translation in translations]

    def getPronunciation(self, word):
        res = self.cursor.execute('SELECT pronunciation FROM chinese_words WHERE word = ?', (word,))
        pronunciation = res.fetchone()
        return pronunciation[0] if pronunciation else None

    def setDB(self, lang):
        if not os.path.isfile(lang):
            raise FileNotFoundError(f'File {lang} was not found, please download it')
        self.conn = sqlite3.connect(lang)
        self.cursor = self.conn.cursor()

    def getAll(self, word):
        definition = self.getDefinition(word)
        pronunciation = self.getPronunciation(word)
        attribute = self.getPos(word)
        translation = self.getTranslation(word)
        return [translation, attribute, definition, pronunciation]
    
    ##PROBABLY NEED A NEW MODULE FOR THIS IMPORTING NATURAL LANGUAGE PROCCESS
    def parseWord(word):
        parsed = word 
        return parsed
    
    def main(self):
        word = "我"
        results = self.getAll(word)
        print(results)

if __name__ == "__main__":
    lang = "/Users/ai/Documents/GitHub/Project/chinese_words.db"
    retriever = retrieval(lang)
    retriever.main()
