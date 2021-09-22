import datetime
import io

import torch
from PIL import Image
from sqlalchemy import func

from db_connect import db
from flask import  Blueprint
import cv2
from keras.models import load_model
import pandas as pd
import detect
from db_models import Target, Flower
import os
import shutil
from flask import request, jsonify
from werkzeug.utils import secure_filename

analyzed = Blueprint('analyzed', __name__)
model = torch.hub.load('/home/ukiiing00/Yolov5/SeochoFlower', 'custom',
                       path='/home/ukiiing00/Yolov5/SeochoFlower/ml/best.pt', source='local')  # local repo

@analyzed.route("/analyze", methods=["GET", "POST"])
def analyze():
    if request.method == "POST":

        imageFile = request.form["src"]
        imageFile = imageFile.rsplit("/")[-1]

        with open("/home/ukiiing00/Yolov5/SeochoFlower/static/img/" + imageFile, 'rb') as f:
            fileRead = f.read()
        img = Image.open(io.BytesIO(fileRead))
        # 이미지파일 임시 저장
        savePath = "/home/ukiiing00/Yolov5/SeochoFlower/datasets/images/train/"  # 매번 비워지는 임시 저장소
        savePath2 = "/home/ukiiing00/Yolov5/SeochoFlower/datasets/images/val/"  # 누적 저장
        if os.path.exists(savePath):
            shutil.rmtree(savePath)  # 파일 삭제
        if not os.path.exists(savePath):
            os.mkdir(savePath)       # 디렉토리 생성

        # 이미지 디텍션을 위한 임시 저장
        img.save(savePath + secure_filename(imageFile))

        with open("/home/ukiiing00/Yolov5/SeochoFlower/static/img/" + imageFile, 'rb') as f:
            fileRead = f.read()
        img = Image.open(io.BytesIO(fileRead))
        img.save(savePath2 + secure_filename(imageFile))

        # imageFile = "C:/Users/jinsung/Downloads/boardtest" + imageFile
        imageFile = imageFile.rsplit("/")[-1]



        # 이미지 디텍션 실행
        detect.run()
        results = model(savePath + secure_filename(imageFile), size=640)  # reduce size=320 for faster inference

        json_data = pd.DataFrame(results.pandas().xyxy[0], columns=["class"])
        result_list = []
        for i in range(0, len(json_data)):
            result_list.append(json_data.values[i][0])

        # 중복 제거
        result_list = set(result_list)
        result_list = list(result_list)

        print(result_list)

        dict={0:'거베라_거베라',
            1: '국화_코스모스',
            2: '국화_디스버드',
            3: '국화_백선',
            4: '튤립_레드',
            5: '튤립_로얄버진',
            6: '백합_메두사',
            7: '백합_시베리아',
            8: '수국_그린',
            9: '수국_핑크',
            10: '데이지_데이지',
            11: '데이지_겹',
            12: '용담_용담',
            13: '장미_푸에고',
            14: '장미_하젤',
            15: '카네이션_핑크',
            16: '카네이션_레드(스프레이)',
            17: '안개_오버타임',
            18: '해바라기_겹',
            19: '해바라기_해바라기',
            20: 'out_of_distribution'}

        flower_list = []
        for i in range(0, len(result_list)):
            if result_list[i] != 20:
                flower_list.append(dict[result_list[i]])
        print(flower_list)
        if flower_list== []:
           flower_list.append('올바른 사진을 넣어주세요')

        return jsonify(flower_list)


@analyzed.route("/image_detect", methods=["GET", "POST"])
def detect_image():
    if request.method == "POST":
        print(request.files)
        # try:
        if 'input-image' in request.files:
            imageFile = request.files['input-image']

        f = imageFile.filename
        # 이미지파일 임시 저장
        savePath = "/home/ukiiing00/Yolov5/SeochoFlower/datasets/images/train/"  # 매번 비워지는 임시 저장소
        savePath2 = "/home/ukiiing00/Yolov5/SeochoFlower/datasets/images/val/"   # 누적 저장
        print('working1')
        if os.path.exists(savePath):
            shutil.rmtree(savePath)  # 파일 삭제
        if not os.path.exists(savePath):
            os.mkdir(savePath)       # 디렉토리 생성

    # 이미지 디텍션을 위한 임시 저장
        imageFile.save(savePath + secure_filename(f))
        imageFile.save(savePath2 + secure_filename(f))

    # 이미지 디텍션 실행
        detect.run()
        # with open(savePath + secure_filename(f), 'rb') as ff:
        #     fileRead = ff.read()
        # img = Image.open(io.BytesIO(fileRead))
        # results = model(img, size=640)  # reduce size=320 for faster inference
        res = model(savePath + secure_filename(f), size=640)
            #img.save(savePath2 + secure_filename(f))

        # except Exception as e:
        #     print('Exception',e)

        result_list = []
        resdata = res.pandas().xyxy[0]
        json_data = pd.DataFrame(resdata, columns=["class"])

        for i in range(0, len(json_data)):
            result_list.append(json_data.values[i][0])

        # 중복 제거
        result_list = set(result_list)
        result_list = list(result_list)

        print(result_list)

        dict={0:'거베라_거베라',
            1: '국화_코스모스',
            2: '국화_디스버드',
            3: '국화_백선',
            4: '튤립_레드',
            5: '튤립_로얄버진',
            6: '백합_메두사',
            7: '백합_시베리아',
            8: '수국_그린',
            9: '수국_핑크',
            10: '데이지_데이지',
            11: '데이지_겹',
            12: '용담_용담',
            13: '장미_푸에고',
            14: '장미_하젤',
            15: '카네이션_핑크',
            16: '카네이션_레드(스프레이)',
            17: '안개_오버타임',
            18: '해바라기_겹',
            19: '해바라기_해바라기',
            20: 'out_of_distribution'}

        flower_list = []
        for i in range(0,len(result_list)):
            flower_list.append(dict[result_list[i]])
        print(flower_list)
        return jsonify(flower_list)


@analyzed.route("/analyse_result", methods=["GET"])
def analyse_image():
    # 꽃 품목_품종 가져오기
    fl_name = request.args.get("flower_name")
    print(fl_name)

    #문자열 스플릿
    fl_item, fl_type = str(fl_name).split('_')

    flist = Target(fl_item, fl_type)
    db.session.add(flist)
    db.session.commit()
    print(flist.fl_item, flist.fl_type)

    # 딕셔너리에 담아서 json 형태로 변환하여 전송
    flower_dict = []

    today = datetime.datetime.today().strftime("%Y-%m-%d")
    fcost = db.session.query(Flower.poomname, Flower.goodname, Flower.lvname, func.sum(Flower.qty).label('qty'),
                             func.avg(Flower.cost).label('cost'), Flower.dateinfo). \
        filter(Flower.poomname == flist.fl_item, Flower.goodname == flist.fl_type). \
        filter(Flower.dateinfo >= func.ADDDATE(today, -7)). \
        group_by(Flower.lvname).all()

    assert isinstance(fcost, object)
    for f in fcost:
        flower_dict.append({
            "poomname": f.poomname,
            "goodname": f.goodname,
            "lvname": f.lvname,
            "cost": int(f.cost),
            "qty": int(f.qty),
            "dateinfo": str(f.dateinfo)
        })
    print(flower_dict)

    return jsonify(flower_dict)