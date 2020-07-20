import sqlite3
from flask import Flask, render_template, g, request, redirect, url_for

DATABASE = 'usda-sqlite-master/usda.sql3'
app = Flask(__name__)


@app.route("/food-group-list")
def food_groups_page():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()
    cur.execute("SELECT * FROM food_group")

    rows = cur.fetchall()
    print(len(rows))
    cur.close()
    return render_template("foodGroup.html", rows=rows)


@app.route("/food-group/<id>")
def food_group_contains_page(id):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()
    cur.execute("SELECT * FROM food WHERE food_group_id = ?", (id,))

    rows = cur.fetchall()
    cur.close()
    return render_template("food_group_contains.html", rows=rows)


@app.route("/food/<id>")
def food_page(id):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()
    cur.execute("SELECT f.*,fg.name FROM food f LEFT JOIN food_group fg ON f.food_group_id=fg.id WHERE f.id = ? ", (id,))
    rows = cur.fetchone()
    cur.close()
    return render_template("food_page.html", rows=rows)


@app.route("/food-edit/<id>", methods=['POST', 'GET'])
def food_edit_page(id):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM food_group")

    groups = cur.fetchall()
    cur.close()

    if request.method == 'GET':
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT f.*,fg.name FROM food f LEFT JOIN food_group fg ON f.food_group_id=fg.id WHERE f.id = ? ", (id,))
        rows = cur.fetchone()
        cur.close()
        return render_template("edit_page.html", groups=groups, rows=rows)

    elif request.method == 'POST':
        foodGroup = request.form['foodGroup']
        shortDescription = request.form['shortDescription']
        longDesc = request.form['longDesc']
        manuf = request.form['manufacturer_name']
        sci_name = request.form['sci_name']

        conn = sqlite3.connect(DATABASE, timeout=20)
        cur = conn.cursor()

        if foodGroup is not None and foodGroup != 0:
            conn = sqlite3.connect(DATABASE, timeout=20)
            cur = conn.cursor()
            cur.execute("UPDATE food SET food_group_id=? WHERE id = ?", (foodGroup, id,))
            conn.commit()
        if shortDescription is not None and shortDescription != "":
            conn = sqlite3.connect(DATABASE, timeout=20)
            cur = conn.cursor()
            cur.execute("UPDATE food SET short_desc=? WHERE id = ?", (shortDescription, id,))
            conn.commit()
        if longDesc is not None and longDesc != "":
            conn = sqlite3.connect(DATABASE, timeout=20)
            cur = conn.cursor()
            cur.execute("UPDATE food SET long_desc=? WHERE id = ?", (longDesc, id,))
            conn.commit()
        if manuf is not None and manuf != "":
            conn = sqlite3.connect(DATABASE, timeout=20)
            cur = conn.cursor()
            conn.commit()
            cur.execute("UPDATE food SET manufac_name=? WHERE id = ?", (manuf, id,))
        if sci_name is not None and sci_name != "":
            conn = sqlite3.connect(DATABASE, timeout=20)
            cur = conn.cursor()
            cur.execute("UPDATE food SET sci_name=? WHERE id = ?", (sci_name, id,))
            conn.commit()

        cur.close()
        return redirect(url_for('food_page', id=id))


@app.route("/")
def home_page():
   return render_template("home_page.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
