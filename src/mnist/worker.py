from mnist.db.dml import dml, select, update
import random
import requests
from datetime import datetime
import pytz
import os
from mnist.model import preprocess_image,predict_digit
#import pdb

# MySQL 연결 코드 중간에 디버깅 트리거
#pdb.set_trace()

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
    try:
        num = one()
        #print(f"one: {num}")
    
        # STEP 2
        # RANDOM 으로 0 ~ 9 중 하나 값을 prediction_result 컬럼에 업데이트
        image_path = "/home/kim1/code/mnist/note/example_2.png"
        predict_result = predict_digit(image_path)
        prediction_time = now_seoul()
        prediction_model = "n22"

        # 동시에 prediction_model, prediction_time 도 업데이트
        predict_set = (predict_result, prediction_model,prediction_time, num)
        result = update_result(*predict_set)
        result_pr = result[0]['prediction_result']
        #print(result_pr)
        # STEP 3
        # LINE 으로 처리 결과 전송
    except:
        result_pr = "처리할 이미지가 필요합니다."

    finally:
        datetime = now_seoul()
        print({"now" :f"{datetime}"})
        send_line(result_pr)
