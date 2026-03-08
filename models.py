from datetime import datetime, timezone
from extensions import db
import enum

class PriorityLevel(enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)


class WishlistItem(db.Model):
    __tablename__ = "wishlist_items"

    id = db.Column(db.Integer, primary_key=True)
    title =db.Column(db.String(200), nullable = False)
    url = db.Column(db.String(500), nullable = False)
    note = db.Column(db.Text, nullable = True)
    price = db.Column(db.Float, nullable = True)
    purchased =db.Column(db.Boolean, default = False, nullable = False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)


class JournalEntry(db.Model):
    __tablename__ = "journal_entries"

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    mood = db.Column(db.String(50), nullable = True)
    content = db.Column(db.String, nullable = False)
    created_at = db.Column(db.DateTime(timezone=True), default = lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)

class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    description = db.Column(db.Text, nullable=True)

    priority = db.Column(db.Enum(PriorityLevel), default = PriorityLevel.MEDIUM, nullable = False)
    is_completed = db.Column(db.Boolean, default = False)

    created_at = db.Column(db.DateTime(timezone=True), default = lambda: datetime.now(timezone.utc))
    deadline = db.Column(db.DateTime(timezone=True), nullable = True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
