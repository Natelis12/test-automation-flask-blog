from helpers import Blueprint, message, redirect, session

logoutBlueprint = Blueprint("logout", __name__)


@logoutBlueprint.route("/logout")
def logout():
    match "userName" in session:
        case True:
            message("2", f'USER: "{session["userName"]}" LOGGED OUT')
            session.clear()
            return redirect("/")
        case False:
            message("1", "USER NOT LOGGED IN")
            return redirect("/")
