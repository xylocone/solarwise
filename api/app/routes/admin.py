from flask import Blueprint, session, redirect, url_for, flash, render_template

# Custom modules
from app.utils.forms import LoginForm
from app.models.user import User
from app.constants import ADMIN_USERNAME, ADMIN_PASSWD

"""
The APIs for accessing admin portal
"""
admin_bp = Blueprint("admin", __name__)


# The route for admin login
@admin_bp.route("/", methods=["GET", "POST"])
def admin():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if username == ADMIN_USERNAME and password == ADMIN_PASSWD:
            # Start the session
            session["name"] = username
            return redirect(url_for("collections"))
        else:
            flash("Invalid credentials, please try again.")
            return redirect(url_for("admin"))

    return render_template("login.jinja", form=form)


# The route for the dashboard for admin


# The collections for the database
@admin_bp.route("/collections")
def collections():
    # If we're not logged-in, then return to login
    if not session.get("name"):
        return redirect(url_for("admin"))

    # Get all the collections in the database
    return render_template("collections.jinja")


@admin_bp.route("/collections/users")
def collection_users():
    # If we're not logged-in, then return to login
    if not session.get("name"):
        return redirect(url_for("admin"))

    # Get the data of the users collection
    fields = User.serialize_fields()

    # Get the data about the users
    users = User.query.all()
    # Serialize all the users
    users = list(map(User.serialize, users))

    return render_template(
        "collections.jinja", fields=map(lambda f: f.get("name"), fields), data=users
    )


# The logs for the database
@admin_bp.route("/logs")
def logs():
    # If we're not logged-in, then return to login
    if not session.get("name"):
        return redirect(url_for("admin"))

    data = None
    with open("app.log", mode="r+") as log_file:
        data = log_file.read().strip().split("\n")
        data = list(map(lambda string: string.split(" - "), data))

    # Return the logs of the current operation
    return render_template("logs.jinja", logs=data)


# The route to logout the admin
@admin_bp.route("/logout")
def logout():
    # Pop the session and redirect to login
    session.pop("name")
    return redirect(url_for("admin"))
