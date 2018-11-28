# documentation-sample

## Get code

```bash
git clone git@github.com:itkr/documentation-sample.git
cd ./documentation-sample
```

## Run server using local Python and Gunicorn

### Install libraries

```bash
pip install -r requirements.txt
```

### Run server

```bash
gunicorn main:app
```

http://localhost:8000/docs/

## Run server using Docker

### Build

```bash
docker build -t docs .
```

### Run

```
docker run --rm -it -p 8000:8000 docs
```

http://localhost:8000/docs/

## Required libraries

| name       | reason                                           |
|------------|--------------------------------------------------|
| docutils   | reStructuredTextを扱う                           |
| gunicorn   | WSGI HTTP Server                                 |
| jinja2     | テンプレートエンジン                             |
| jsonschema | JSONSchemaを扱う                                 |
| paste      | ローカルでwebサーバーを動かす                    |
| pygments   | reStructuredTextでコードブロックを扱うときに使用 |
| webapp2    | Webフレームワーク                                |
| webob      | webapp2で使用                                    |
