from dbChecker import POSTS_DB, USERS_DB
from helpers import Blueprint, redirect, render_template, session, sqlite3

adminPanelPostsBlueprint = Blueprint("adminPanelPosts", __name__)


@adminPanelPostsBlueprint.route("/admin/posts")
@adminPanelPostsBlueprint.route("/adminpanel/posts")
def adminPanelPosts():
    match "userName" in session:
        case True:
            connection = sqlite3.connect(USERS_DB)
            cursor = connection.cursor()
            cursor.execute(
                f'select role from users where userName = "{session["userName"]}"'
            )
            role = cursor.fetchone()[0]
            match role == "admin":
                case True:
                    connection = sqlite3.connect(POSTS_DB)
                    cursor = connection.cursor()
                    cursor.execute("select * from posts")
                    posts = cursor.fetchall()
                    return render_template(
                        "dashboard.html", posts=posts, showPosts=True
                    )
                case False:
                    return redirect("/")
        case False:
            return redirect("/")
