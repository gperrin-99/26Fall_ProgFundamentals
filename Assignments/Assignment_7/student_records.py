import sqlite3
conn = sqlite3.connect("student_records.db")

cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS StudentRecords")
cur.execute("""
   CREATE TABLE StudentRecords (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        major TEXT NOT NULL
    )
""")

students = [
    (1, "Alice Johnson", 20, "Computer Science"),
    (2, "Bob Smith", 22, "Mathematics"),
    (3, "Charlie Brown", 19, "Physics"),
    (4, "Diana Prince", 21, "Chemistry"),
    (5, "Ethan Hunt", 23, "Biology"),
]
cur.executemany(
    "INSERT INTO StudentRecords VALUES (?, ?, ?, ?)", students
)
conn.commit()

print("\nAll students on record:")
cur.execute("SELECT name, age, major FROM StudentRecords")
for name, age, major in cur.fetchall():
    print(f"Name: {name}, Age: {age}, Major: {major}")

while True:
    add_student = input(
        "\nDo you want to add a new student? (yes/no): "
    ).strip().lower()
    if add_student in ("yes", "no"):
        break

if add_student == "yes":
    while True:
        new_name = input("Enter the student's name: ").strip()
        if new_name:
            break
        print("Name cannot be empty.")

    while True:
        age_input = input("Enter the student's age: ").strip()
        try:
            new_age = int(age_input)
            if new_age < 0:
                raise ValueError
            break
        except ValueError:
            print("Age must be a whole number.")

    while True:
        new_major = input("Enter the student's major: ").strip()
        if new_major:
            break
        print("Major cannot be empty.")

    cur.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM StudentRecords")
    new_id = cur.fetchone()[0]
    cur.execute(
        "INSERT INTO StudentRecords (id, name, age, major) "
        "VALUES (?, ?, ?, ?)",
        (new_id, new_name, new_age, new_major),
    )
    conn.commit()
    print(
        f"\nNew student record added: {new_name}, "
        f"Age: {new_age}, Major: {new_major}"
    )

conn.close()