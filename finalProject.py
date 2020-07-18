import sqlite3
from flask import Flask, render_template, g


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
    return render_template("foodGroup.html", rows=rows)


@app.route("/food-group/<id>")
def food_group_contains_page(id):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()
    cur.execute("SELECT * FROM food WHERE food_group_id = ?", (id,))

    rows = cur.fetchall()
    return render_template("food_group_contains.html", rows=rows)


@app.route("/food")
def food_page(id):
    return render_template("food_group_contains.html")


@app.route("/")
def home_page():
   return render_template("home_page.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
