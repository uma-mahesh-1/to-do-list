from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('todo.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        task TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

# Home page: Display tasks
@app.route('/')
def index():
    conn = sqlite3.connect('todo.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasks')
    tasks = cur.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# Add a new task
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        task = request.form['task']
        conn = sqlite3.connect('todo.db')
        cur = conn.cursor()
        cur.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

# Update a task
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    conn = sqlite3.connect('todo.db')
    cur = conn.cursor()
    cur.execute('SELECT task FROM tasks WHERE id = ?', (id,))
    task = cur.fetchone()[0]
    conn.close()

    if request.method == 'POST':
        new_task = request.form['task']
        conn = sqlite3.connect('todo.db')
        cur = conn.cursor()
        cur.execute('UPDATE tasks SET task = ? WHERE id = ?', (new_task, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('update.html', task=task, id=id)

# Delete a task
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('todo.db')
    cur = conn.cursor()
    cur.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
