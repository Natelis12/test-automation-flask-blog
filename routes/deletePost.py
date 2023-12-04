from dbChecker import POSTS_DB
from helpers import Blueprint, message, redirect, session, sqlite3

deletePostBlueprint = Blueprint("deletePost", __name__)


@deletePostBlueprint.route("/deletepost/<int:postID>/redirect=<direct>")
def deletePost(postID, direct):
    direct = direct.replace("&", "/")
    match "userName" in session:
        case True:
            connection = sqlite3.connect(POSTS_DB)
            cursor = connection.cursor()
            cursor.execute(f"select author from posts where id = {postID}")
            author = cursor.fetchone()
            match author[0] == session["userName"]:
                case True:
                    cursor.execute(f"delete from posts where id = {postID}")
                    cursor.execute("update sqlite_sequence set seq = seq-1")
                    connection.commit()
                    message("2", f'POST: "{postID}" DELETED')
                    return redirect("/")
                case False:
                    message(
                        "1",
                        f'POST: "{postID}" NOT DELETED "{postID}" DOES NOT BELONG '
                        f'TO USER: {session["userName"]}',
                    )
                    return redirect("/")
            return redirect(f"/{direct}")
        case False:
            message("1", f'USER NEEDS TO LOGIN FOR DELETE POST: "{postID}"')
            return redirect(f"/login/redirect=&post&{postID}")
