
from flask import redirect, request, render_template, jsonify, Blueprint, session, g
from db_models import User, Post
from db_connect import db
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import os
import datetime

board = Blueprint('board', __name__)
bcrypt = Bcrypt()


@board.before_app_request
def load_logged_in_user():
    user_id = session.get("login")
    if login is None:
        g.user = None
    else:
        g.user = db.session.query(User).filter(User.id == user_id).first()

@board.route("/",methods=['GET'])
def home():
    # # 없으면 login으로
    # if session.get('login') is None:
    #     #session['login'] -> 없으면 오류
    #     return redirect("/login")
    # # 있으면 post로
    # else:
        #return redirect("/post")
    data = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("main.html", post_list=data)

@board.route("/gallery")
def gallery():
    data = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("gallery.html", post_list=data)

@board.route("/post", methods=["GET", "POST"])
def post():
    if session.get('login') is not None:
        if request.method == 'GET':
            # GET 요청이 오는 경우의 코드를 작성하세요.
            data = Post.query.order_by(Post.created_at.desc()).all()
            return render_template("test.html", post_list = data)
        else:
            print('request_file', request.files)
            if 'input-image' in request.files:
                imageFile = request.files['input-image']
                # 이미지파일 임시 저장
                savePath = "/home/ukiiing00/Yolov5/SeochoFlower/static/img/"

                content = request.form['content']
                author = request.form['author']
                today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                imagename = author + today + ".jpg"
                # 유저네임 + 게시 시간 이름으로
                imageFile.save(savePath + secure_filename(imagename))

                print(imagename)

                post = Post(author, content, imagename)
                db.session.add(post)
                db.session.commit()

                return jsonify({"result": "success"})

            else:
                today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                content = request.form['content']
                author = request.form['author']
                post = Post(author, content, today)
                db.session.add(post)
                db.session.commit()

                return jsonify({"result": "success"})

    else:
        return redirect("/")

@board.route("/join", methods=["GET", "POST"])
def join():
    if session.get("login") is None:
        if request.method == 'GET':
            return render_template('join.html')
        else:
            user_id = request.form['user_id']
            user_pw = request.form['user_pw']
            pw_hash = bcrypt.generate_password_hash(user_pw)

            user = User(user_id, pw_hash)
            db.session.add(user)
            db.session.commit()
            return jsonify({"result": "success"})
    else:
        return redirect("/")

# 로그인을 위한 login() 함수를 완성하세요.
@board.route("/login", methods=['GET', 'POST'])
def login():
    if session.get("login") is None:
        if request.method == 'GET':
            return render_template('login.html')
        else:
            user_id = request.form['user_id']
            user_pw = request.form['user_pw']
            user = User.query.filter(User.user_id == user_id).first()

            if user is not None:
                if bcrypt.check_password_hash(user.user_pw, user_pw):
                    session['login'] = user.id
                    return jsonify({"result": "success"})
                else:
                    return jsonify({"result": "fail"})
            else:
                return jsonify({"result": "fail"})
    else:
        return redirect("/")

@board.route("/logout")
def logout():
    session['login'] = None
    return redirect("/")



@board.route("/post", methods=["DELETE"])
def delete_post():
    # 글을 삭제하는 기능을 완성하세요.
    id = request.form['id']
    author = request.form['author']
    data = Post.query.filter(Post.id == id, Post.author == author).first()
    if data is not None:
        db.session.delete(data)
        db.session.commit()
        return jsonify({"result":"success"})
    else:
        return jsonify({"result":"fail"})

@board.route("/post", methods=["PATCH"])
def update_post():
    # 글을 수정하는 기능을 완성하세요.
    id = request.form['id']
    content = request.form['content']
    author = User.query.filter(User.id == session['login']).first()

    data = Post.query.filter(Post.id == id, Post.author == author.user_id).first()
    data.content = content
    db.session.commit()
    return jsonify({"result":"success"})


@board.route("/like", methods=["PATCH"])
def update_like():
    id = request.form['id']
    post = Post.query.filter(Post.id == id).first()
    post.likeit += 1
    db.session.commit()

    return jsonify({'result': 'success'})
