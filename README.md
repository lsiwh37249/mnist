# mnist

### RUN
```bash
$ uvicorn src.mnist.main:app --reload
```

### DB
```bash
sudo docker run -d \
        --name mnist-mariadb \
        -e MARIADB_USER=mnist \
        --env MARIADB_PASSWORD=1234 \
        --env MARIADB_DATABASE=mnistdb \
        --env MARIADB_ROOT_PASSWORD=my-secret-pw \
        -p 53306:3306 \
        mariadb:latest
```

### Docker 
```bash
sudo docker run -p 8022:8080 --name mnist22 \
-v /home/ubuntu/images:/home/ubuntu/images \
-e UPLOAD_DIR=/home/ubuntu/images/n22 \
-e DB_IP=172.17.0.1 \
-e LINE_NOTI_TOKEN=goYUCNhbAw9hMwaiTGs7m3sFyqQxi313CzaLTDODdtA lsiwh37249/mnist:0.4.0
```
