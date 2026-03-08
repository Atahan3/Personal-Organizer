from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from utils import login_required
from extensions import db
from models import JournalEntry

journal_bp = Blueprint("journal", __name__)

@journal_bp.route("/journal", methods= ['GET', 'POST'])
@login_required
def list_and_add_journal():
    if request.method == 'POST':
        title = request.form.get('title', "").strip()
        mood = request.form.get('mood', "").strip()
        content = request.form.get('content').strip()
        if not title or not content:
            flash("Title and content are required", "error")
            return redirect(url_for("journal.list_and_add_journal"))


        new_entry = JournalEntry(title =title,
                                   mood = mood,
                                   content = content,
                                   user_id = session["user_id"]
                                   )
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for("journal.list_and_add_journal"))

    entries = JournalEntry.query.filter_by(user_id=session["user_id"]).order_by(JournalEntry.created_at.desc()).all()
    return render_template("journal.html",entries = entries)

@journal_bp.route("/journal/toggle/<int:entry_id>", methods = ['GET', 'POST'])
@login_required
def entry_toggle(entry_id):
    if request.method == 'POST':

        entry = db.session.get(JournalEntry, entry_id)
        if entry and entry.user_id == session["user_id"]:
            entry.title = request.form.get("title")
            entry.content = request.form.get("content")
            db.session.commit()
            return redirect(url_for('journal.list_and_add_journal'))

@journal_bp.route("/journal/delete/<int:entry_id>", methods =['POST'])
@login_required
def delete_entry(entry_id):
    entry = JournalEntry.query.get_or_404(entry_id)
    if entry.user_id != session["user_id"]:
        return "unauthorized", 403
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for("journal.list_and_add_journal"))

