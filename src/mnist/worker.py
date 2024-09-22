from mnist.db.dml import dml, select, update
import random
import requests
from datetime import datetime
import pytz
import os

def one():
    sql = """SELECT * FROM image_processing WHERE prediction_result IS NULL ORDER BY num LIMIT 2"""
    result = select(query=sql, size=1)
    return result[0]['num']

def update_result(*p):
    sql_u = """UPDATE image_processing SET prediction_result = %s, prediction_model = %s,prediction_time= %s WHERE num = %s"""
    update(sql_u,*p)
    sql_s = f"SELECT * FROM image_processing WHERE num = {p[3]}"
    result = select(sql_s,1)
    return result

def now_seoul():
    time = datetime.now(pytz.timezone('Asia/Seoul'))
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time

def send_line(messages):
    token = os.getenv('LINE_NOTI_TOKEN')
    headers = {'Authorization': f'Bearer {token}'}
    info = {'message': f'predict_result : {messages}'}
    response = requests.post('https://notify-api.line.me/api/notify', headers=headers, data = info)

def run():
    # STEP 1
    # image_processing 테이블의 prediction_result IS NULL 인 ROW 1 개 조회 - num 갖여오기
    num = one()
    print(f"one: {num}")
    
    # STEP 2
    # RANDOM 으로 0 ~ 9 중 하나 값을 prediction_result 컬럼에 업데이트
    predict_result = random.randrange(0,10)
    prediction_time = now_seoul()
    prediction_model = "simple_random"

    # 동시에 prediction_model, prediction_time 도 업데이트
    predict_set = (predict_result, prediction_model,prediction_time, num)
    result = update_result(*predict_set)
    result_pr = result[0]['prediction_result']
    print(result_pr)
    # STEP 3
    # LINE 으로 처리 결과 전송
    send_line(result_pr)
