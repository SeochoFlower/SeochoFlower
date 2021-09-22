"""
Run a rest API exposing the yolov5s object detection model
"""
from db_connect import db
from flask import Flask, render_template
from board_api import board
from page_api import page
from analyze_api import analyzed
from kakao_api import kakao

import os

app = Flask(__name__)
app.register_blueprint(board)
app.register_blueprint(page)
app.register_blueprint(analyzed)
app.register_blueprint(kakao)

# db = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='ai_college', charset="utf8")
# cur = db.cursor()  # 커서 클래스 호출

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://ukiiing00:****@host-endpoint:3306/ai_college"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.secret_key = os.urandom(24)


db.init_app(app)



if __name__ == "__main__":
    # hubconf.py 경로, best.pt 경로
    app.run(host='0.0.0.0', port=5000, debug=True)  # debug=True causes Restarting with stat
