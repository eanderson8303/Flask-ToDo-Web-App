import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def init_db():
    #Connect to the dabase
    conn = sqlite3.connect("todo.db")
    #Allow execution of SQL commands
    c = conn.cursor()
    #Create a table named 'tasks' if it doesn't already exist
    #Create an id that automatically increments to uniquely identify tasks
    #Create a content of a text column that stores tasks
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    ''')
    #Save any changes to the database
    conn.commit()
    #Closes connection to avoid any memory/resource issues
    conn.close()

# Call the database once when the app starts
init_db()

#Define homepage route
#Handle both GET (normal page load) and POST (form submission) requests
@app.route("/", methods=["GET", "POST"])
def home():
    #Open database and get a cursor to execute SQL commands
    conn = sqlite3.connect("todo.db")
    c = conn.cursor()

    #If user submitted the form -> pull text from form -> inset into database -> save changes
    #Pull text
    if request.method == "POST":
        #Insert into database (tasks table)
        task = request.form["task"]
        c.execute("INSERT INTO tasks (content) VALUES (?)", (task,))
        #Save changes
        conn.commit()

    # Fetch all tasks to show
    c.execute("SELECT * FROM tasks") #gets all rows from the 'tasks' table
    tasks = c.fetchall() # returns a list of tuples
    conn.close() #closes database connection

    #Render HTML file
    return render_template("index.html", tasks=tasks)


#Delete Route
@app.route("/delete/<int:task_id>")
#Delete function
def delete(task_id):
    #Connect to DB
    conn = sqlite3.connect("todo.db")
    #Grab cursor to execute SQL
    c = conn.cursor()
    #Send delete command
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,)) #Parameterized query to prevent SQL injection
    #Save changes
    conn.commit()
    #Close connection
    conn.close()
    #Return to homepage
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
