from dbChecker import COMMENTS_DB, USERS_DB
from helpers import Blueprint, redirect, render_template, session, sqlite3

adminPanelCommentsBlueprint = Blueprint("adminPanelComments", __name__)


@adminPanelCommentsBlueprint.route("/admin/comments")
@adminPanelCommentsBlueprint.route("/adminpanel/comments")
def adminPanelComments():
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
                    connection = sqlite3.connect(COMMENTS_DB)
                    cursor = connection.cursor()
                    cursor.execute("select * from comments")
                    comments = cursor.fetchall()
                    return render_template("adminPanelComments.html", comments=comments)
                case False:
                    return redirect("/")
        case False:
            return redirect("/")
