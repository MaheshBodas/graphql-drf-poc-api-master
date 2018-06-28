from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
 
"""class RiskFieldTypeEnum(ChoiceEnum):
class RiskFieldTypeEnum(Enum):
    text = "text"
    date = "date"
    integer = "integer"
    number = "number"
    currency = "currency"
 """
# Create your models here.
# class user(AbstractUser):
#    None    

class risktype(models.Model):
    createdby = models.ForeignKey(User, related_name='user_risktypes', on_delete=models.CASCADE,null=True, blank=True)
    risk_type_name = models.CharField(max_length=100, unique=True,
            error_messages={
                'unique': 'risk_type_name must be unique'
            })
    risk_type_description = models.CharField(max_length=100, blank=True, default='')

    def get_RiskTypeFields(self):
        risktypefields = risktypefield.objects.filter(risktype=self)        
        return risktypefields
    

class risktypefield(models.Model):    
    """ risk_type_field_name = models.CharField(max_length=100,unique=True,
            error_messages={
                'unique': 'risk_type_field_name must be unique within and across risk Types'
            }) """
    risk_type_field_name = models.CharField(max_length=100)
    #risk_type_field_enum = EnumChoiceField(enum_class=RiskFieldTypeEnum , default=RiskFieldTypeEnum.text)
    risk_type_field_enum = models.CharField(max_length=10, blank=True, default='')
    risk_type_field_description = models.CharField(max_length=100, blank=True, default='')
    risktype = models.ForeignKey(risktype, related_name='risktype_risktypefields', on_delete=models.CASCADE,null=True, blank=True)    


    

class risk(models.Model):
    createdby = models.ForeignKey(User, related_name='user_risks', on_delete=models.CASCADE,null=True, blank=True)      
    risk_name = models.CharField(max_length=100, unique=True,
            error_messages={
                'unique': 'risk_name must be unique'
            })
    risk_description = models.CharField(max_length=100, blank=True, default='')    
    risktype = models.ForeignKey(risktype,on_delete=models.CASCADE,null=True, blank=True)
    @property
    def risk_type_id(self):
        self.risktype.id
    @property
    def risk_type_name(self):
        self.risktype.risk_type_name

class riskfield(models.Model):
    risk_field_value = models.CharField(max_length=100, blank=True, default='')  
    # Field is of type risktypefield    
    
    risktypefield = models.ForeignKey(risktypefield,on_delete=models.CASCADE,null=True, blank=True)
    risk = models.ForeignKey(risk, related_name='risk_riskfields', on_delete=models.CASCADE,null=True, blank=True)


    #   
    @property
    def risk_type_field_id(self):
        self.risktypefield.risk_type_field_id
    @property
    def risk_type_field_name(self):
        self.risktypefield.risk_type_field_name
    @property
    def risk_type_field_enum(self):
        self.risktypefield.risk_type_field_enum
    #