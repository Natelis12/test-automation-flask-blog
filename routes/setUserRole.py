from dbChecker import USERS_DB
from helpers import Blueprint, message, redirect, session, sqlite3

setUserRoleBlueprint = Blueprint("setUserRole", __name__)


@setUserRoleBlueprint.route("/setuserrole/<userName>/<newRole>")
def setUserRole(userName, newRole):
    match "userName" in session:
        case True:
            connection = sqlite3.connect(USERS_DB)
            cursor = connection.cursor()
            cursor.execute(
                f'select role from users where userName = "{session["userName"]}"'
            )
            role = cursor.fetchone()[0]
            match role == "admin":
                case  True:
                    cursor.execute(
                        f'update users set role = "{newRole}" where lower(userName) = '
                        f'"{userName.lower()}" ')
                    connection.commit()
                    message(
                        "2", f'ADMIN: "{session["userName"]}" CHANGED USER: "{userName}"s ROLE TO '
                             f'{newRole}')
                    return redirect("/admin/users")
                case False:
                    return redirect("/")
        case False:
            return redirect("/")
