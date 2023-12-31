from dbChecker import POSTS_DB, USERS_DB
from helpers import (
    Blueprint, createPostForm, currentDate, currentTime, flash, message, redirect, render_template,
    request, session, sqlite3
)

editPostBlueprint = Blueprint("editPost", __name__)


@editPostBlueprint.route("/editpost/<int:postID>", methods=["GET", "POST"])
def editPost(postID):
    match "userName" in session:
        case True:
            connection = sqlite3.connect(POSTS_DB)
            cursor = connection.cursor()
            cursor.execute("select id from posts")
            posts = str(cursor.fetchall())
            match str(postID) in posts:
                case True:
                    connection = sqlite3.connect(POSTS_DB)
                    cursor = connection.cursor()
                    cursor.execute(f"select * from posts where id = {postID}")
                    post = cursor.fetchone()
                    message("2", f'POST: "{postID}" FOUND')
                    connection = sqlite3.connect(USERS_DB)
                    cursor = connection.cursor()
                    cursor.execute(
                        f'select userName from users where userName="{session["userName"]}"'
                    )
                    match post[4] == session["userName"]:
                        case True:
                            form = createPostForm(request.form)
                            form.postTitle.data = post[1]
                            form.postTags.data = post[2]
                            form.postContent.data = post[3]
                            if request.method == "POST":
                                postTitle = request.form["postTitle"]
                                postTags = request.form["postTags"]
                                postContent = request.form["postContent"]
                                match postContent == "":
                                    case True:
                                        flash("post content not be empty", "error")
                                        message(
                                            "1",
                                            f'POST CONTENT NOT BE EMPTY USER: '
                                            f'"{session["userName"]}"',
                                        )
                                    case False:
                                        connection = sqlite3.connect(POSTS_DB)
                                        cursor = connection.cursor()
                                        cursor.execute(
                                            f'update posts set title = '
                                            f'"{postTitle}" where id = {post[0]}'
                                        )
                                        cursor.execute(
                                            f'update posts set tags = '
                                            f'"{postTags}" where id = {post[0]}'
                                        )
                                        cursor.execute(
                                            f'update posts set content = '
                                            f'"{postContent}" where id = {post[0]}'
                                        )
                                        cursor.execute(
                                            f'update posts set lastEditDate = '
                                            f'"{currentDate()}" where id = {post[0]}'
                                        )
                                        cursor.execute(
                                            f'update posts set lastEditTime = '
                                            f'"{currentTime()}" where id = {post[0]}'
                                        )
                                        connection.commit()
                                        message("2", f'POST: "{postTitle}" EDITED')
                                        flash("Post edited", "success")
                                        return redirect(f"/post/{post[0]}")

                            return render_template(
                                "/editPost.html",
                                title=post[1],
                                tags=post[2],
                                content=post[3],
                                form=form,
                            )
                        case False:
                            flash("this post not yours", "error")
                            message(
                                "1",
                                f'THIS POST DOES NOT BELONG TO USER: "{session["userName"]}"',
                            )
                            return redirect("/")
                case False:
                    message("1", f'POST: "{postID}" NOT FOUND')
                    return render_template("404.html")
        case False:
            message("1", "USER NOT LOGGED IN")
            flash("you need login for edit a post", "error")
            return redirect("/login")
