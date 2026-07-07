import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

app = Flask(__name__)

# Core security configuration
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Bind the tracker database
db = SQL("sqlite:///tracker.db")

# Admin configuration
ADMIN_USER = "#####"

# In-memory blog store
BLOGS = [
    {
        "id": 1,
        "title": "Mastering the Stipendium Hungaricum Motivation Letter",
        "tag": "Scholarships",
        "reading_time": 5,
        "content": "<p>A structured breakdown of writing strong statement letters for European undergraduate funding paths.</p>"
    },
    {
        "id": 2,
        "title": "Balancing Digital SAT Prep and IELTS Milestones",
        "tag": "Testing Strategy",
        "reading_time": 4,
        "content": "<p>A clear, practical guide on managing dual test preparation profiles.</p>"
    }
]

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def is_admin():
    """Helper to check if current user is the administrator."""
    user = db.execute("SELECT username FROM users WHERE id = ?", session.get("user_id"))
    return user and user[0]["username"] == ADMIN_USER

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    apps = db.execute("SELECT * FROM applications WHERE user_id = ? ORDER BY deadline ASC", user_id)
    scores = db.execute("SELECT * FROM test_scores WHERE user_id = ?", user_id)
    return render_template("index.html", apps=apps, scores=scores)

@app.route("/calendar")
@login_required
def calendar():
    user_id = session["user_id"]
    apps = db.execute("SELECT * FROM applications WHERE user_id = ? ORDER BY deadline ASC", user_id)
    return render_template("calendar.html", apps=apps)

@app.route("/blogs")
def blogs():
    return render_template("blogs.html", posts=BLOGS)

@app.route("/edit-blog", methods=["GET", "POST"])
@login_required
def edit_blog():
    # Admin-only check
    if not is_admin():
        flash("Access Denied: Only the administrator can edit blogs.")
        return redirect(url_for("blogs"))

    if request.method == "POST":
        blog_id = request.form.get("blog_id")
        title = request.form.get("title")
        tag = request.form.get("tag")
        reading_time = request.form.get("reading_time")
        content = request.form.get("content") # Receives HTML from Quill

        if not title or not tag or not reading_time or not content:
            flash("Please fill out all fields.")
            return redirect(url_for("blogs"))

        if blog_id:
            for post in BLOGS:
                if str(post["id"]) == str(blog_id):
                    post.update({"title": title, "tag": tag, "reading_time": int(reading_time), "content": content})
                    break
        else:
            new_id = max([b["id"] for b in BLOGS]) + 1 if BLOGS else 1
            BLOGS.append({"id": new_id, "title": title, "tag": tag, "reading_time": int(reading_time), "content": content})
        return redirect(url_for("blogs"))

    return render_template("edit_blog.html", post=next((b for b in BLOGS if str(b["id"]) == str(request.args.get("id"))), None))

@app.route("/delete-blog/<int:blog_id>", methods=["POST"])
@login_required
def delete_blog(blog_id):
    if not is_admin():
        flash("Access Denied.")
        return redirect(url_for("blogs"))

    global BLOGS
    BLOGS = [b for b in BLOGS if b["id"] != blog_id]
    return redirect(url_for("blogs"))

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) == 1 and check_password_hash(rows[0]["hash"], password):
            session["user_id"] = rows[0]["id"]
            return redirect(url_for("index"))
        flash("Invalid username or password.")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or password != request.form.get("confirmation"):
            flash("Registration error.")
            return render_template("register.html")
        if db.execute("SELECT * FROM users WHERE username = ?", username):
            flash("Username taken.")
            return render_template("register.html")

        # Fixed: Insert with empty strings for all potential NOT NULL schema requirements
        db.execute("INSERT INTO users (username, hash, first_name, last_name, email) VALUES(?, ?, ?, ?, ?)",
                   username, generate_password_hash(password), "", "", "")
        session["user_id"] = db.execute("SELECT id FROM users WHERE username = ?", username)[0]["id"]
        return redirect(url_for("index"))
    return render_template("register.html")

@app.route("/add-application", methods=["GET", "POST"])
@login_required
def add_application():
    if request.method == "POST":
        db.execute("INSERT INTO applications (user_id, institution, program, scholarship_name, deadline, status) VALUES (?, ?, ?, ?, ?, ?)",
                   session["user_id"], request.form.get("institution"),
                   request.form.get("custom_degree") if request.form.get("degree_program") == "Other" else request.form.get("degree_program"),
                   request.form.get("scholarship"), request.form.get("deadline"), request.form.get("status"))
        return redirect(url_for("index"))
    return render_template("add_application.html")

@app.route("/add-test", methods=["GET", "POST"])
@login_required
def add_test():
    if request.method == "POST":
        db.execute("INSERT INTO test_scores (user_id, test_type, target_score, current_score, test_date) VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], request.form.get("test_type"), request.form.get("target"),
                   request.form.get("current"), request.form.get("test_date"))
        return redirect(url_for("index"))
    return render_template("add_test.html")

@app.route("/delete/<string:table>/<int:entry_id>", methods=["POST"])
@login_required
def delete_entry(table, entry_id):
    if table in ["applications", "test_scores"]:
        db.execute(f"DELETE FROM {table} WHERE id = ? AND user_id = ?", entry_id, session["user_id"])
    return redirect(url_for("index"))
