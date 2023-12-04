from dbChecker import USERS_DB
from helpers import Blueprint, redirect, render_template, session, sqlite3

adminPanelUsersBlueprint = Blueprint("adminPanelUsers", __name__)


@adminPanelUsersBlueprint.route("/admin/users")
@adminPanelUsersBlueprint.route("/adminpanel/users")
def adminPanelUsers():
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
                    connection = sqlite3.connect(USERS_DB)
                    cursor = connection.cursor()
                    cursor.execute("select * from users")
                    users = cursor.fetchall()
                    return render_template(
                        "adminPanelUsers.html",
                        users=users,
                    )
                case False:
                    return redirect("/")
        case False:
            return redirect("/")
