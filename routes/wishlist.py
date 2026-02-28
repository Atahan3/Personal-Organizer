from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort

from utils import login_required
from extensions import db
from models import WishlistItem
wishlist_bp = Blueprint("wishlist", __name__)


@wishlist_bp.route("/wishlist", methods = ['GET','POST'])
@login_required
def list_and_add_wishlist():
    if request.method == 'POST':
        title = (request.form.get('title') or "").strip()
        url = (request.form.get('url') or "").strip()
        price_raw = (request.form.get('price') or "").strip()
        note = (request.form.get('note') or "").strip() or None

        if not title or not url:
            flash("Title and URL are required.", "error")
            return redirect(url_for("wishlist.list_and_add_wishlist"))

        price = None
        if price_raw:
            try:
                price = float(price_raw.replace(",","."))
            except ValueError:
                flash("Price must be numeric.", "error")
                return redirect(url_for("wishlist.list_and_add_wishlist"))

        new_item = WishlistItem(title=title,
                                url = url,
                                price= price,
                                note = note,
                                purchased = False,
                                user_id = session["user_id"])
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('wishlist.list_and_add_wishlist'))
    items = WishlistItem.query.filter_by(user_id=session["user_id"]).order_by(WishlistItem.created_at.desc()).all()
    return render_template("wishlist.html", items =items)

@wishlist_bp.route("/wishlist/delete/<int:item_id>", methods = ['POST'])
@login_required
def delete_item(item_id):
    item = WishlistItem.query.get_or_404(item_id)

    if item.user_id != session["user_id"]:
        return "Unauthorized", 403
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("wishlist.list_and_add_wishlist"))

@wishlist_bp.route("/wishlist/toggle/<int:item_id>", methods = ['POST'])
@login_required
def toggle_wishlist(item_id):
    item = WishlistItem.query.get_or_404(item_id)
    if item.user_id != session["user_id"]:
        return "Unauthorized", 403
    item.purchased = not item.purchased
    db.session.commit()
    return redirect(url_for("wishlist.list_and_add_wishlist"))

@wishlist_bp.route("/wishlist/edit/<int:item_id>", methods = ['GET','POST'])
@login_required
def edit_wishlist(item_id):

    item = WishlistItem.query.get_or_404(item_id)

    if item.user_id != session["user_id"]:
        return "Unauthorized", 403

    if request.method == 'POST':
        title = (request.form.get('title') or "").strip()
        url = (request.form.get('url') or "").strip()
        price_raw = (request.form.get('price') or "").strip()
        note = (request.form.get('note') or "").strip() or None

        if not title or not url:
            flash("Title and URL are required.", "error")
            return redirect(url_for("wishlist.edit_wishlist", item_id =item_id))

        price = None
        if price_raw:
            try:
                price = float(price_raw.replace(",", "."))
            except ValueError:
                flash("Price must be numeric.", "error")
                return redirect(url_for("wishlist.edit_wishlist", item_id=item_id))
        item.title = title
        item.url = url
        item.price = price
        item.note = note
        db.session.commit()
        return redirect(url_for("wishlist.list_and_add_wishlist"))

    return render_template("edit_item.html", item = item)