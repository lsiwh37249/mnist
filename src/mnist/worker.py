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
    sql = """SELECT * FROM image_processing WHERE prediction_result IS NULL ORDER BY num LIMIT 1"""
    result = select(query=sql, size=1)
    return (result[0]['num'], result[0]['file_path'])

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
    info = {'message': f'predict_result : {messages[0]}, label : {messages[1]}'}
    response = requests.post('https://notify-api.line.me/api/notify', headers=headers, data = info)

def run():
    # STEP 1
    # image_processing 테이블의 prediction_result IS NULL 인 ROW 1 개 조회 - num 갖여오기
    num,image_path = one()
    
    if num is None:
      print(f"{jigeum.seoul.now()} - job is None")
      return
    
    # STEP 2
    # RANDOM 으로 0 ~ 9 중 하나 값을 prediction_result 컬럼에 업데이트
    #image_path = "/home/kim1/code/mnist/img/2eba341a-d3dd-47dd-8fba-b446158bfa79.png"
    predict_result = predict_digit(image_path)
    print(f"predict_result : {predict_result}")
    prediction_time = now_seoul()
    prediction_model = "n22"

    # 동시에 prediction_model, prediction_time 도 업데이트
    predict_set = (predict_result, prediction_model,prediction_time, num)
    result = update_result(*predict_set)
    result_pr = (result[0]['prediction_result'], result[0]['label'])
    # STEP 3
    # LINE 으로 처리 결과 전송
    datetime = now_seoul()
    print({"now" :f"{datetime}"})
    send_line(result_pr)
