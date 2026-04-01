from mylibrary.task_utils import format_task

from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('tasks.db')
    conn.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, name TEXT)')
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('tasks.db')
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = format_task(request.form['task'])
    conn = sqlite3.connect('tasks.db')
    conn.execute('INSERT INTO tasks (name) VALUES (?)', (task,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('tasks.db')
    conn.execute('DELETE FROM tasks WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    new_task = request.form['updated_task']
    conn = sqlite3.connect('tasks.db')
    conn.execute('UPDATE tasks SET name=? WHERE id=?', (new_task, id))
    conn.commit()
    conn.close()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
