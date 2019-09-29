import graphene
import riskapi.schema
from graphene_django.debug import DjangoDebug

class Query(
    riskapi.schema.Query,    
    graphene.ObjectType,
):
    debug = graphene.Field(DjangoDebug, name="_debug")

class Mutation(riskapi.schema.Mutation, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    debug = graphene.Field(DjangoDebug, name="_debug")

schema = graphene.Schema(query=Query, mutation=Mutation, auto_camelcase=False,)
# schema = graphene.Schema(query=Query, auto_camelcase=False,)

