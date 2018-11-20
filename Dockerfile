FROM ubuntu:18.04
MAINTAINER itkr itkrst@gmail.com
LABEL title="documentation-by-jsonschema"
LABEL description="documentation-by-jsonschema"

# 環境変数

ENV TZ "Asia/Tokyo"
ENV PYTHONIOENCODING "utf-8"

# 依存モジュールインストール

RUN apt update -y
RUN apt install -y python-dev python-pip

# コードコピー

ARG PROJECT_PATH=/root
WORKDIR ${PROJECT_PATH}
COPY . ${PROJECT_PATH}/

# Pythonライブラリ

RUN pip install -r requirements.txt

# 実行コマンド

EXPOSE 8000

CMD ["gunicorn", "--bind=0.0.0.0:8000", "main:app"]
