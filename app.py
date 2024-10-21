from flask import Flask, render_template, request, g
import sqlite3

app = Flask(__name__)

DATABASE = 'fleet.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/')
def index():
    tables = query_db("SELECT name FROM sqlite_master WHERE type='table';")
    return render_template('home.html', tables=tables)


@app.route('/table/<table_name>')
def view_table(table_name):
    rows = query_db(f'SELECT * FROM {table_name}')

    cur = get_db().execute(f'SELECT * FROM {table_name}')
    colnames = [description[0] for description in cur.description]
    return render_template('tables.html', rows=rows, colnames=colnames, table_name=table_name)




