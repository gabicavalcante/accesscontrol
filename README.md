# accesscontrol

### create and active virtualenv 

```
virtualenv -p python3 env
source env/bin/activate
```

### install requirements

```
cd accesscontrol
pip install -r requirements.txt
```

### create and configure .env file

```
touch .env     
```

add the env vars:

```
FLASK_APP=app.py
APP_SETTINGS="config.DevelopmentConfig"
DATABASE_URL="postgresql://localhost/accesscontrol"
```


### run 

```
flask run
```