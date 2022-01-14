from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
tasks = SQLAlchemy(app)


class Task(tasks.Model):
    id = tasks.Column(tasks.Integer, primary_key=True)
    title = tasks.Column(tasks.String(100))
    complete = tasks.Column(tasks.Boolean)


@app.route("/")
def home():
    task_list = Task.query.all()
    return render_template("app.html", task_list=task_list)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_task = Task(title=title, complete=False)
    tasks.session.add(new_task)
    tasks.session.commit()
    return redirect(url_for("home"))


@app.route("/update/<int:task_id>")
def update(task_id):
    task = Task.query.filter_by(id=task_id).first()
    task.complete = not task.complete
    tasks.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:task_id>")
def delete(task_id):
    task = Task.query.filter_by(id=task_id).first()
    tasks.session.delete(task)
    tasks.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    tasks.create_all()
    app.run(debug=True)
