
from flask import Blueprint, request, session, jsonify, render_template
from sphinx.util import requests

kakao = Blueprint('kakao', __name__)



@kakao.route("/kakaopay/paymethod.ajax", methods=['POST'])
def paymethod():
    if request.method == 'POST':
        poomName = request.form["poomName"]
        goodName = request.form["goodName"]
        lvName = request.form["lvName"]
        qty = request.form["qty"]
        cost = request.form["cost"]
        cost = int(qty) * int(cost)
        shop = request.form["shop"]
        print(shop)

        URL = 'https://kapi.kakao.com/v1/payment/ready'
        headers = {
            'Authorization': "KakaoAK " + "fd80f4dc1c2efac96c80e2d4e2666cba",
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        params = {
            "cid": "TC0ONETIME",
            "item_code": str(shop),
            "partner_order_id": "1001",
            "partner_user_id": "testuser",
            "item_name": str(poomName) + " " + str(goodName) + " " + str(lvName) ,
            "quantity": str(qty),
            "total_amount": str(cost),
            "tax_free_amount": 0,
            "vat_amount": 200,
            "approval_url": "http://35.216.39.230:5000/kakaopay/success",
            "cancel_url": "http://35.216.39.230:5000/kakaopay/cancel",
            "fail_url": "http://35.216.39.230:5000/kakaopay/fail",
        }

        res = requests.post(URL, headers=headers, params=params)
        print(res)
        session['tid'] = res.json()['tid']
        next_url = res.json()['next_redirect_pc_url']

        return jsonify({'next_url': res.json()['next_redirect_pc_url']})

    return render_template('index.html')


@kakao.route("/kakaopay/success", methods=['POST', 'GET'])
def sucess():
    URL = 'https://kapi.kakao.com/v1/payment/approve'
    headers = {
        "Authorization": "KakaoAK " + "fd80f4dc1c2efac96c80e2d4e2666cba",
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }
    params = {
        "cid": "TC0ONETIME",  # 테스트용 코드
        "tid": session['tid'],  # 결제 요청시 세션에 저장한 tid
        "partner_order_id": "1001",  # 주문번호
        "partner_user_id": "testuser",  # 유저 아이디
        "pg_token": request.args.get("pg_token"),  # 쿼리 스트링으로 받은 pg토큰
    }
    res = requests.post(URL, headers=headers, params=params)

    print(res.text)
    print(res.json())
    print(res.json()['amount'])
    print(res.json()['amount']['total'])
    amount = res.json()['amount']['total']
    res = res.json()
    context = {
        'res': res,
        'amount': amount,
    }
    return render_template('success.html', context=context, res=res)