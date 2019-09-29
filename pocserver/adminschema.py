import graphene
import riskapi.schema
from graphene_django.debug import DjangoDebug

class AdminQuery(
    riskapi.schema.AdminQuery,    
    graphene.ObjectType,
):
    debug = graphene.Field(DjangoDebug, name="_debug")

class AdminMutation(riskapi.schema.AdminMutation, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    debug = graphene.Field(DjangoDebug, name="_debug")

schema = graphene.Schema(query=AdminQuery, mutation=AdminMutation, auto_camelcase=False,)


