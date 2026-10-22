import sqlite3
conn = sqlite3.connect('library.db')
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS books")

cur.execute("""
    CREATE TABLE books 
    (id   INT NOT NULL,
    title TEXT REQUIRED,
    author TEXT REQUIRED,
    year INT REQUIRED,
    genre TEXT REQUIRED,
    copies INT REQUIRED,
    rating INT,
    PRIMARY KEY (id))
""")

cur.execute("INSERT INTO books VALUES (1, 'To Kill a Mockingbird', 'Harper Lee', 1960, 'Fiction', 5, 4.8)")

books = [
    (2, '1984', 'George Orwell', 1949, 'Dystopian', 3, 4.7),
    (3, 'The Great Gatsby', 'F. Scott Fitzgerald', 1925, 'Fiction', 4, None),
    (4, 'Pride and Prejudice', 'Jane Austen', 1813, 'Romance', 2, 4.6),
    (5, 'The Catcher in the Rye', 'J.D. Salinger', 1951, 'Fiction', 6,None),
    (6, 'The Hobbit', 'J.R.R. Tolkien', 1937, 'Fantasy', 7, 4.9),
    (7, 'Fahrenheit 451', 'Ray Bradbury', 1953, 'Dystopian', 4, 4.3),
    (8, 'Eragon', 'Christopher Paolini', 2002, 'Fantasy', 5, 5.0),
]

cur.executemany("INSERT INTO books VALUES (?,?,?,?,?,?,?)", books)

conn.commit()

print("\nAll books published after 1990:")
cur.execute("SELECT * FROM books WHERE year > 1990")
for row in cur.fetchall():
    print(row)


print("\nAll fiction books with more than 2 copies:")
cur.execute("SELECT * FROM books WHERE genre = 'Fiction' AND copies > 2")
for row in cur.fetchall():
    print(row)


print("\nAll books published before 1900 or rated 5:")
cur.execute("SELECT * FROM books WHERE year < 1900 OR rating = 5")
for row in cur.fetchall():
    print(row)

print("\nAll books not in the 'Mystery' genre:")
cur.execute("SELECT * FROM books WHERE genre != 'Mystery'")
for row in cur.fetchall():
    print(row)

print("\nAll books in either the Science or History genres:")
cur.execute("SELECT * FROM books WHERE genre IN ('Science', 'History')")
for row in cur.fetchall():
    print(row)

letter=input("\nEnter a letter to find an author whose name starts with that letter: ")
search_query=f"{letter}%"
query = "SELECT * FROM books WHERE author LIKE ?"
cur.execute(query, (search_query,))
authors = cur.fetchall()

if authors:
    print(f"\nAuthors whose names start with '{letter}':")
    for author in authors:
        print(author)

print("\nAll books with out a rating:")
cur.execute("SELECT * FROM books WHERE rating IS NULL")
for row in cur.fetchall():
    print(row)

conn.close()
