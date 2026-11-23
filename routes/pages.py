from flask import Blueprint, render_template

# HTML pages wale routes - api wale routes alag file me hain
pages = Blueprint("pages", __name__)


@pages.get("/")
def index():
    # poora app ek hi page pe hai: 3 steps, JS unko switch karta hai
    return render_template("index.html")