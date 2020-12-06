Points = {"A": 1,"B": 3,"C": 3,"D": 2,"E": 1,"F": 4,"G": 2,"H": 4,"I": 1,"J": 1,"K": 5,
                 "L": 1,"M": 3,"N": 1,"O": 1,"P": 3,"Q": 10,"R": 1,"S": 1,"T": 1,
                 "U": 1,"V": 4,"W": 4,"X": 8,"Y": 4,"Z": 10}

from cs50 import SQL

db = SQL("sqlite:///words.db")

# source: https://www.mit.edu/~ecprice/wordlist.10000
with open("ScrabbleDic.txt") as f:
    words = f.read().splitlines()

def calculate(word):
    score = 0
    for letter in word:
        score += Points[letter]
    return score


for word in words:
    db.execute("INSERT INTO dictionary (word, value) VALUES(?,?)", word, calculate(word))