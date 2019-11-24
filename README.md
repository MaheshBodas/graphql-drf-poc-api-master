# DJango GraphQL PoC API Server

Source code for the [DJango GraphQL PoC Server][server].

[server]: https://github.com/MaheshBodas/graphql-drf-poc-api-master

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)


GraphQL based API to for defining RiskTypes and Risk Instances based on RiskType

  - API allows users to create RiskTypes and associated RiskTypeFields
in one go with use of nested serializer.
  - During creation of Risk Instance system checks that proper referential integrity
is maintained with Risk Type.
  - While creation of Risk Fields system ensures that proper referential integrity is 
  maintained with Risk and Risk Type fields.
  - Risk API allows users to create Risk and associated RiskFields in one
go with use of nested serializer.
  - Various model validation errors in RiskType and RiskTypeFields, Risk
and RiskFields are returned to client of serve API in JSON format.
  - Used Graphene DJango library to expose all of API over single endpoint.
  - Added new View class to the application so as to avoid unauthenticated access to GraphQL queries and mutation.  
  Default GraphQLView in Graphene library allows access to all of the users.
  - GraphQL has concept of queries i.e. Client application defines shape of data to be retried from server. Using Graphene-Django library we can define Query and Resolver classes. Thus root element in GraphQL query map to one of the resolver class which is further used to get and filter data from underlying Django model.
  - GraphQL Mutations, Input types are used for adding and updating Django Models. Made use of Django serializers in DRF to do all validation before committing model changes.
  - Added DJango Admin support to Import and Export RiskTypes and Risk Instances.

### For details of User guide refer following links
- [User Guide](https://github.com/MaheshBodas/graphql-drf-poc-api-master/tree/master/blob/graphql-drf-poc-api-master-user-guide.pdf)
- [Sample GraphQL Queries and Mutations](https://github.com/MaheshBodas/graphql-drf-poc-api-master/tree/master/blob/graphql-query.txt)

### It makes use of following technology.
- DJango Rest Framework, Graphene-DJango library.
- Deployed to Heroku platform.

### Installation

```sh
$ mkvirtualenv graphql-drf-poc-api-master
$ setprojectdir .
$ git clone https://github.com/MaheshBodas/graphql-drf-poc-api-master
$ workon drf-poc-api-master 
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
