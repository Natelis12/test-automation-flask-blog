from helpers import Blueprint, redirect, render_template, session, sqlite3

adminPanelBlueprint = Blueprint("adminPanel", __name__)


@adminPanelBlueprint.route("/admin")
def adminPanel():
    match "userName" in session:
        case True:
            connection = sqlite3.connect("db/users.db")
            cursor = connection.cursor()
            cursor.execute(
                f'select role from users where userName = "{session["userName"]}"'
            )
            role = cursor.fetchone()[0]
            match role == "admin":
                case True:
                    return render_template("adminPanel.html")
                case False:
                    return redirect("/")
        case False:
            return redirect("/")
