from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from utils import login_required
from extensions import db
from models import Task, PriorityLevel
from datetime import datetime

task_bp = Blueprint("tasks", __name__)

@task_bp.route("/task", methods = ['GET', 'POST'])
@login_required
def new_task():
    if request.method == 'POST':
        title = request.form.get("title")
        description = request.form.get("description")
        priority_input = request.form.get("priority")
        deadline_input = request.form.get("deadline")

        if not title:
            flash("Enter a title", "error")
            return redirect(url_for("tasks.new_task"))
        priority = PriorityLevel.MEDIUM
        if priority_input == "Low":
            priority = PriorityLevel.LOW
        elif priority_input == "High":
            priority = PriorityLevel.HIGH

        deadline = None
        if deadline_input:
            try:
                deadline = datetime.strptime(deadline_input, '%Y-%m-%d')
            except ValueError:
                flash("Invalid date format", "error")


        new_task_object = Task(
            title = title,
            description = description,
            priority = priority,
            deadline = deadline,
            user_id = session["user_id"]
        )
        db.session.add(new_task_object)
        db.session.commit()
        flash("Task added successfully!", "success")
        return redirect(url_for("tasks.new_task"))
    tasks = Task.query.filter_by(user_id=session["user_id"]).order_by(
        Task.is_completed.asc(),
        Task.deadline.asc()
    ).all()

    return render_template('tasks.html', tasks = tasks)

@task_bp.route("/tasks/toggle/<int:task_id>", methods = ['GET', 'POST'])
@login_required
def task_toggle(task_id):
    task = db.session.get(Task, task_id)
    if task and task.user_id == session["user_id"]:
        task.is_completed = not task.is_completed
        db.session.commit()
        return  redirect(url_for('tasks.new_task'))

@task_bp.route("/tasks/delete/<int:task_id>", methods = ['GET', 'POST'])
@login_required
def task_delete(task_id):
    task = Task.query.get_or_404(task_id)
    if task and task.user_id == session["user_id"]:
        db.session.delete(task)
        db.session.commit()
        flash("Task deleted successfully", "success")
    return redirect(url_for("tasks.new_task"))