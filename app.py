import os

from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_session import Session

from extensions import db

from werkzeug.security import check_password_hash, generate_password_hash

from utils import login_required
from routes.wishlist import wishlist_bp
from routes.journal import journal_bp
from routes.task_manager import task_bp

app = Flask(__name__)
app.secret_key=os.environ.get("SECRET_KEY","ultra_mega_secret_key?:)")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL","sqlite:///test.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] =False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = { "pool_pre_ping": True}
db.init_app(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

app.register_blueprint(wishlist_bp)
app.register_blueprint(journal_bp)
app.register_blueprint(task_bp)

from models import User, WishlistItem, JournalEntry, Task, PriorityLevel


with app.app_context():
    db.create_all()


@app.route("/")
def index():
   if "user_id" in session:
       return redirect(url_for('profile'))
   return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = (request.form.get('username') or "").strip()
        password = request.form.get('password') or ""

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            session["username"] = user.username
            next_page = request.form.get("next") or "/"
            if not next_page.startswith("/"):
                next_page = "/"
            return redirect(next_page)
        flash("wrong password or username please try again", "error")
        return redirect("/login")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("session cleared successfully", "success")
    return redirect("/login")


@app.route("/profile", methods =["GET", "POST"])
@login_required
def profile():
    user = db.session.get(User, session["user_id"])
    return render_template("profile.html", user=user)


@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            flash("username and password required", "error")
            return redirect("/register")
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("this username already occupied", "error")
            return redirect("/register")
        password_hash = generate_password_hash(password)

        new_user = User(username = username, password_hash = password_hash)
        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.id
        session["username"] = new_user.username

        flash("Registration completed successfully", "success")
        return redirect("/profile")
    return render_template("register.html")





if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)