FROM ubuntu:18.04
MAINTAINER itkr itkrst@gmail.com
LABEL title="documentation-by-jsonschema"
LABEL description="documentation-by-jsonschema"

# 環境変数

ENV TZ "Asia/Tokyo"
ENV PYTHONIOENCODING "utf-8"

# 依存モジュールインストール

RUN apt update -y
#RUN apt install -y python3-dev python3-pip wget unzip gnupg curl
RUN apt install -y python-dev python-pip wget unzip gnupg curl

# コードコピー

ARG PROJECT_PATH=/root
WORKDIR ${PROJECT_PATH}
COPY . ${PROJECT_PATH}/

# Pythonライブラリ

#RUN pip3 install -r requirements.txt
RUN pip install -r requirements.txt

# 実行コマンド

#ENTRYPOINT ["python3", "main.py"]
#ENTRYPOINT ["python", "main.py"]
ENTRYPOINT ["gunicorn", "main:app"]
