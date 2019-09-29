import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.debug import DjangoDebug
from graphene_django.rest_framework.mutation import SerializerMutation
from riskapi.models import RiskType, RiskTypeField, Risk, RiskField
from django.contrib.auth.models import User
from riskapi.serializers import RiskTypeSerializer, RiskTypeFieldSerializer, RiskSerializer, RiskFieldSerializer


class UserQL(DjangoObjectType)  :
    class Meta:
        model = User
        exclude = ('password',)

class RiskTypeQL(DjangoObjectType):
    class Meta:
        model = RiskType
     

class RiskTypeFieldQL(DjangoObjectType):
    class Meta:
        model = RiskTypeField
        exclude = ('risktype',)

    risktype = graphene.String()
    def resolve_risktype(self, info):
        return self.risktype.id  




class RiskQL(DjangoObjectType):
    class Meta:
        model = Risk        
        exclude = ('risktype',)        

    risktype = graphene.Int()
    def resolve_risktype(self, info):
        return self.risktype.id 
    
    risk_type_name = graphene.String()
    def resolve_risk_type_name(self, info):
        return self.risktype.risk_type_name 

class RiskFieldQL(DjangoObjectType):
    class Meta:
        model = RiskField
        exclude = ('risktypefield',)

    risk = graphene.String()
    def resolve_risk(self, info):
        return self.risk.id   

    risktypefield = graphene.String()
    def resolve_risktypefield(self, info):
        return self.risktypefield.id

    risk_type_field_name = graphene.String()
    def resolve_risk_type_field_name(self, info):
        return self.risktypefield.risk_type_field_name 

    risk_type_field_enum = graphene.String()
    def resolve_risk_type_field_enum(self, info):
        return self.risktypefield.risk_type_field_enum 

    
# Create Input Object Types
class RiskTypeFieldInput(graphene.InputObjectType):        
    risk_type_field_name = graphene.String()
    risk_type_field_enum = graphene.String()
    risk_type_field_description = graphene.String()

class RiskTypeInput(graphene.InputObjectType):        
    risk_type_name = graphene.String()
    risk_type_description = graphene.String()
    risktype_risktypefields = graphene.List(RiskTypeFieldInput)

# Create mutations for actors
class CreateRiskType(graphene.Mutation):
    class Arguments:
        input = RiskTypeInput(required=True)
    ok = graphene.Boolean()
    risktype = graphene.Field(RiskTypeQL)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        serializer = RiskTypeSerializer(data=input)
        serializer.is_valid(raise_exception=True)
        returnData = serializer.save()
        # serializer.save()
        return CreateRiskType(ok=ok, risktype=returnData)

#
class RiskFieldInput(graphene.InputObjectType):        
    risktypefield = graphene.Int()
    risk_field_value = graphene.String()

class RiskInput(graphene.InputObjectType):        
    risktype = graphene.Int()
    risk_name = graphene.String()
    risk_description = graphene.String()
    risk_riskfields = graphene.List(RiskFieldInput)

class CreateRisk(graphene.Mutation):
    class Arguments:
        input = RiskInput(required=True)
    ok = graphene.Boolean()
    risk = graphene.Field(RiskQL)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        serializer = RiskSerializer(data=input)
        serializer.is_valid(raise_exception=True)
        returnData = serializer.save()
        # serializer.save()
        return CreateRisk(ok=ok, risk=returnData)

class AdminMutation(graphene.ObjectType):
    create_risktype = CreateRiskType.Field()
    create_risk = CreateRisk.Field() 

class Mutation(graphene.ObjectType):
    create_risk = CreateRisk.Field() 

#     

class CommonQuery(object):
    
    user = graphene.Field(UserQL, id=graphene.Int(), username=graphene.String())

    risktype = graphene.Field(RiskTypeQL, id=graphene.Int(), risk_type_name=graphene.String(), 
                                risk_type_description=graphene.String())
    
    risktypefield = graphene.Field(RiskTypeFieldQL)

    risk = graphene.Field(
        RiskQL, id=graphene.Int(), risk_name=graphene.String(), risk_description=graphene.String(), risktype=graphene.Int()
    )

    all_users = graphene.List(UserQL)

    all_risks = graphene.List(RiskQL, risktype=graphene.Int())
    
    def resolve_all_users(self, context):
        # We can easily optimize query count in the resolve method
        return User.objects.all()
    
    def resolve_user(self, context, id=None, username=None):
        if id is not None:
            return User.objects.get(pk=id)

        if username is not None:
            return User.objects.get(username=username)
        
        return None  
    
    def resolve_all_risks(self, context, risktype=None):
        # Filter based on risktype if available
        if risktype is not None:
            allrisks = Risk.objects.select_related("risktype").all()
            return allrisks.filter(risktype=risktype)

        # We can easily optimize query count in the resolve method
        return Risk.objects.select_related("risktype").all()

    
    def resolve_risk(self, context, id=None, risk_name=None, risktype=None):
        if id is not None:
            return Risk.objects.get(pk=id)

        if risk_name is not None:
            return Risk.objects.get(risk_name=risk_name)

        if risktype is not None:
            return Risk.objects.get(risktype=risktype)

        return None    

class AdminQuery(CommonQuery):
    all_risktypes = graphene.List(RiskTypeQL)    
    
    def resolve_risktypefield(self, info, **kwargs):        
        risk_type_field_name = kwargs.get('risk_type_field_name')
        risk_type_field_enum = kwargs.get('risk_type_field_name')
        slug = risk_type_field_name + '_' + risk_type_field_enum
        if slug is not None:
            return RiskTypeField.objects.get(pk=slug)

        return None    

    def resolve_all_risktypes(self, context):
        return RiskType.objects.all()
    
    def resolve_risktype(self, context, id=None, risk_type_name=None):
        if id is not None:
            return RiskType.objects.get(pk=id)

        if risk_type_name is not None:
            return RiskType.objects.get(risk_type_name=risk_type_name)

        return None    

class Query(CommonQuery):
    debug = graphene.Field(DjangoDebug, name="_debug")



# class RiskTypeMutation(SerializerMutation):
#     class Meta:
#         serializer_class = RiskTypeSerializer
#         model_operations = ['create']
#         lookup_field = 'id'

# class RiskTypeFieldMutation(SerializerMutation):
#     class Meta:
#         serializer_class = RiskTypeFieldSerializer
#         model_operations = ['create']
#         lookup_field = 'id'
         
