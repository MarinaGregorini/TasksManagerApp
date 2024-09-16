from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../database/tasks.db"
db = SQLAlchemy(app)

class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    done = db.Column(db.Boolean)

with app.app_context():
    db.create_all()
    db.session.commit()

@app.route("/", methods=["GET"])
def home():
    all_tasks = Task.query.all()
    return render_template("index.html", tasks_list=all_tasks)

@app.route("/create_task", methods=["POST"])
def criar():
    task = Task(content=request.form["task_content"], done=False)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete_task/<id>")
def delete(id):
    task = Task.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/task_done/<id>")
def done(id):
    task = Task.query.filter_by(id=int(id)).first()
    task.done = not(task.done)
    db.session.commit()
    return redirect(url_for("home"))

app.run()