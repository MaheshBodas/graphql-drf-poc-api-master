# DJango REST PoC API Server drf-poc-api-master

Source code for the [DJango REST PoC Server][server].

[server]: https://github.com/MaheshBodas/drf-poc-api-master

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)


REST based API to for defining RiskTypes and Risk

  - Post RiskTypes and Risk
  - Get RiskTypes, RiskTypeKeys, RiskKeys
  - Get Single Risk, All Risks

### Installation

```sh
$ mkvirtualenv britecore-poc-api
$ setprojectdir .
$ git clone https://github.com/MaheshBodas/drf-poc-api-master
$ workon britecore-poc-api 
$ python manage.py makemigrations riskapi
$ python manage.py migrate
S python manage.py shell
```

Creating superuser

```sh
$ manage.py createsuperuser --username=mahesh.bodas --email=mahesh.bodas@gmail.com
$ manage.py createsuperuser --username=root --email=root@example.com --noinput
```
To Run test cases
```sh 
$ python manage.py test riskapi
```
Running application locally
```sh 
$ manage.py runserver localhost:9527
$ manage.py runserver 127.0.0.1:9527
```
Run following code to deploy it to AWS (zappa_settings.json is in repository)
```sh 
$ pip install zappa
$ set AWS_ACCESS_KEY_ID={Your AWS_ACCESS_KEY_ID}
$ set AWS_SECRET_ACCESS_KEY={Your AWS_SECRET_ACCESS_KEY}
$ set AWS_DEFAULT_REGION={Your preferred region}
$ zappa deploy dev