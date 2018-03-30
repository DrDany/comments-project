import sqlite3 as sql
import random
from faker import Factory

fake = Factory.create('ru_RU')

if __name__ == "__main__":
    databaseFile = 'database.sqlite'
    sqlFile = 'init_script.sql'

    try:
        print("Opening DB")
        con = sql.connect(databaseFile)
        cursor = con.cursor()

        print("Reading initial Script...")
        scriptFile = open(sqlFile, 'r', encoding="utf-8")
        script = scriptFile.read()
        scriptFile.close()

        print("Running Script...")
        cursor.executescript(script)
        con.commit()

        for num in range(10):
            fullname = fake.name().split()
            name = fullname[1]
            surname = fullname[0]
            patronymic = fullname[2]
            city = random.randrange(1, 9, 1)
            phone = fake.phone_number()
            email = fake.email()
            comment = fake.text()
            cursor.execute("INSERT INTO main.comments(surname, name, patronymic, city, phone, mail, comment) VALUES(?, ?, ?, ?, ?, ?, ?)",
                (surname, name, patronymic, city, phone, email, comment))
        con.commit()
        print("Record successfully added")
    except Exception as e:
        con.rollback()
        print("Error execute migrations: ", e)
    finally:
        con.close()