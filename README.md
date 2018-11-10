# documentation-by-jsonschema

## Get code

```bash
git clone git@gitlab.com:itkr/documentation-by-jsonschema.git
```

## Install libraries

```bash
cd ./documentation-by-jsonschema
pip install -r requirements.txt
```

## Run server

```bash
gunicorn main:app
```

## Access

http://localhost:8000/docs/
