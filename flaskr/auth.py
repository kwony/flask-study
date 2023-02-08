from crypt import methods
import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

"""
Blueprint
api path랑 앱과 관련된 함수들이 애플리케이션에 등록할 수 있는 모음집이라고 보면 된다.

예로, create_app 안에 @app.route 는 요구사항이 늘어날수록 매핑되는 함수가 끊임없이 늘어날 수 있는데
Blueprint를 활용하면 구조적으로 분리해서 관리할 수 있다.

spring, nestjs의 controller 개념이라고 보면 된다

"""
bp = Blueprint(
    "auth", __name__, url_prefix="/auth"
)  # view와 code를 연결해준다고 하는데 사실상 컨트롤러 같은 개념으로 보면 될 것 같다.


@bp.route("/register", methods=("GET", "POST"))  # auth/register 요청을 처리한다.
def register():
    if request.method == "POST":
        # request.form 은 dict 타입으로 되어있다.
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))
        flash(error)
    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user where username = ?", (username,)
        ).fetchone()

        print("user", user)

        if user is None:
            error = "Incorrect username"
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password"

        if error is None:
            session.clear()
            session["user_id"] = user[
                "id"
            ]  # request 에 대한 데이터를 저장하는 용도. 브라우저 쿠키에 저장된다. 브라우저 용도도 같이 가져갈 떄 써먹음
            return redirect(url_for("index"))
        flash(error)

    return render_template("auth/login.html")


# 요런거 미들웨어로 쓰면 됨. 그런데 매번 이렇게 넣어줘야해...?
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# edit, write, delete 처럼 로그인이 필요한 곳에서 서용하려고 쓰는 미들웨어
def login_requred(view):
    print("login_required called")

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs) 

    return wrapped_view
