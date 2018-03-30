import sqlite3 as sql
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.sqlite")


def get_all_comments():
    con = sql.connect(db_path)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT c.id, c.surname, c.name, c.patronymic, ct.city, r.region, c.phone, c.mail, c.comment " +
                "FROM main.comments c LEFT JOIN  main.cities ct ON ct.id = c.city LEFT JOIN main.regions r ON ct.region = r.id;")
    comments = cur.fetchall()
    con.close()
    return comments


def get_all_regions():
    con = sql.connect(db_path)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM main.regions;")
    regions = cur.fetchall()
    con.close()
    return regions


def get_city_by_region_id(id):
    con = sql.connect(db_path)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM main.cities WHERE region = ?", [id])
    city = cur.fetchall()
    con.close()
    return city


def add_new_comment(surname, name, patronymic, city, phone, mail, comment):
    con = sql.connect(db_path)
    cur = con.cursor()
    cur.execute("INSERT INTO main.comments(surname, name, patronymic, city, phone, mail, comment) "
                "VALUES(?, ?, ?, ?, ?, ?, ?)", (surname, name, patronymic, city, phone, mail, comment))
    con.commit()


def delete_comment_by_id(id):
    con = sql.connect(db_path)
    cur = con.cursor()
    cur.execute("DELETE FROM main.comments WHERE id = ?", [id])
    con.commit()


def update_comment_by_id(surname, name, patronymic, city, phone, mail, comment, id):
    con = sql.connect(db_path)
    cur = con.cursor()
    cur.execute(
        "UPDATE main.comments SET surname = ?, name = ?, patronymic = ? , city = ? , phone =? , mail = ?, comment = ? WHERE id = ?",
        (surname, name, patronymic, city, phone, mail, comment, id))
    con.commit()


def get_comment_by_id(id):
    con = sql.connect(db_path)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute(
        "SELECT c.id AS comment_id, ct.id AS city_id, r.id AS region_id, c.surname, c.name, c.patronymic, ct.city, r.region, c.phone, c.mail, c.comment "
        "FROM main.comments c "
        "LEFT JOIN  main.cities ct ON ct.id = c.city "
        "LEFT JOIN main.regions r ON ct.region = r.id WHERE c.id = ?;", [id])
    comment = cur.fetchone()
    con.close()
    return comment


def get_regions_comment_count(count):
    con = sql.connect(db_path)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute(
        "SELECT DISTINCT (r.region) FROM comments c "
        "LEFT JOIN cities ct ON c.city = ct.id "
        "LEFT JOIN regions r ON r.id = ct.region "
        "GROUP BY r.region HAVING  Count(c.city) > ?;", [count])
    regions = cur.fetchall()
    con.close()
    return regions


def get_comment_count_by_regions():
    con = sql.connect(db_path)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute(
        "SELECT r.id, r.region, COUNT (r.id) AS count  "
        "FROM comments c "
        "LEFT JOIN cities ct ON c.city = ct.id "
        "LEFT JOIN regions r ON r.id = ct.region GROUP BY r.id")
    comments = cur.fetchall()
    con.close()
    return comments


def get_region_by_id(id):
    con = sql.connect(db_path)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute(
        "SELECT * FROM regions WHERE id = ?", [id])
    region = cur.fetchone()
    con.close()
    return region


def get_comment_count_by_region_id(id):
    con = sql.connect(db_path)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute(
        "SELECT ct.*, COUNT (ct.id) AS count  "
        "FROM comments c "
        "LEFT JOIN cities ct ON c.city = ct.id "
        "LEFT JOIN regions r ON r.id = ct.region "
        "WHERE r.id = ? GROUP BY ct.id", [id])
    comments = cur.fetchall()
    con.close()
    return comments
