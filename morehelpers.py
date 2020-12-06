from cs50 import SQL
db = SQL("sqlite:///words.db")
start = db.execute("SELECT word FROM dictionary WHERE word LIKE ? AND LENGTH(word) < 9 ORDER BY value DESC", "A%")
print(start)