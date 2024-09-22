from typing import Annotated
from fastapi import FastAPI, File, UploadFile
import os
import pymysql.cursors

app = FastAPI()

def get_conn():
    con = pymysql.connect(host='172.18.0.1',
                             user='mnist',
                             password='1234',
                             database='mnistdb',
                             port=53306,
                             cursorclass=pymysql.cursors.DictCursor)
    return con

def time_seoul():
    from datetime import datetime
    import pytz

    time = datetime.now(pytz.timezone('Asia/Seoul'))
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time

def select(query: str, size = -1):
    conn = get_conn()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchmany(size)

    return result

# def insert_row(connection, sql, file_name, file_full_path, formatted_time, request_user):
#     with connection.cursor() as cursor:
#         # Create a new record
#         cursor.execute(sql, (file_name, file_full_path, formatted_time, request_user))

#     # connection is not autocommit by default. So you must commit to save
#     # your changes
#     connection.commit()

@app.get("/one")
def one():
    sql = """SELECT * FROM image_processing WHERE prediction_time IS NULL ORDER BY num LIMIT 1"""
    result = select(query=sql, size=1)
    return result[0]

@app.get("/many/")
def many(size: int = -1):
    from mnist.db import get_conn
    sql = "SELECT * FROM image_processing WHERE prediction_time IS NULL ORDER BY num"
    conn = get_conn()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchmany(size)
    return result

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    # 파일 저장
    img = await file.read()
    file_name = file.filename
    print(file_name)

    upload_dir = "/home/kim1/code/mnist/img" 
    # 디렉토리가 없으면 오류, 코드에서 확인 및 만들기 추가
    if not os.path.exists(upload_dir):
        os.mkdir(upload_dir)

    file_full_path = os.path.join(upload_dir, file_name)
    
    with open(file_full_path, "wb") as f:
        f.write(img)
    
    # 시간
    
    from datetime import datetime
    import pytz

    time = datetime.now(pytz.timezone('Asia/Seoul'))
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S")
    
    con = get_conn()

    sql = "INSERT INTO `image_processing` (`file_name`, `file_path`,`request_time`,`request_user`) VALUES (%s, %s, %s, %s)"
    
    from mnist.db.dml import dml
    #values = [file_name, file_full_path, formatted_time, "n22"] 
    insert_row = dml(sql, file_name, file_full_path, formatted_time, "n22")
    
    #이미지 경로로 이미지 받아오기 
    #select_db(file_full_path)


    # 파일 저장 경로 DB INSERT
    # tablename : image_processing
    # 컬럼 정보 : num (초기 인서트, 자동 증가)
    # 컬럼 정보 : 파일이름, 파일경로, 요청시간(초기 인서트), 요청사용자(n00)
    # 컬럼 정보 : 예측모델, 예측결과, 예측시간(추후 업데이트)
    return {
            "filename": file.filename,
            "content_type": file.content_type,
            "file_full_path": file_full_path
           }
