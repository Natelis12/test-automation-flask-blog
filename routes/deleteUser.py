from dbChecker import USERS_DB
from helpers import Blueprint, message, redirect, session, sqlite3

deleteUserBlueprint = Blueprint("deleteUser", __name__)


@deleteUserBlueprint.route("/admin/deleteuser/<userName>/redirect=<direct>")
def deleteUser(userName, direct):
    direct = direct.replace("&", "/")
    match "userName" in session:
        case True:
            connection = sqlite3.connect(USERS_DB)
            cursor = connection.cursor()
            cursor.execute(
                f'select * from users where lower(userName) = "{userName.lower()}"'
            )
            user = cursor.fetchone()
            if not user:
                message("1", f'USER: "{userName}" NOT FOUND')
                return redirect(f"/{direct}")
            cursor.execute(
                f'select role from users where userName = "{session["userName"]}"'
            )
            perpetrator = cursor.fetchone()
            match user:
                case _:
                    match user[1] == session["userName"] or perpetrator[0] == "admin":
                        case True:
                            cursor.execute(
                                f'delete from users where lower(userName) = "{userName}"'
                            )
                            cursor.execute("update sqlite_sequence set seq = seq-1")
                            connection.commit()
                            message("2", f'USER: "{userName}" DELETED')
                            match perpetrator[0] == "admin":
                                case True:
                                    return redirect(f"{direct}")
                                case False:
                                    session.clear()
                                    return redirect(f"{direct}")
                        case False:
                            message(
                                "1",
                                f'USER: "{user[1]}" NOT DELETED YOU ARE NOT {user[1]}',
                            )
                            return redirect(f"{direct}")

        case False:
            message("1", f"USER NEEDS TO LOGIN FOR DELETE USER: {userName}")
            return redirect(f"/login/redirect=&deleteuser&{userName}&redirect=index")
