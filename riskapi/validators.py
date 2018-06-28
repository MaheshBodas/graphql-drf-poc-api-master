import datetime
from rest_framework import serializers,fields
from rest_framework.serializers import ValidationError
from .utils import *

class ValidationUtils:
    @staticmethod
    def list_duplicates(seq):
        seen = set()
        seen_add = seen.add
        # adds all elements it doesn't know yet to seen and all other to seen_twice
        seen_twice = set( x for x in seq if x in seen or seen_add(x) )
        # turn the set into a list (as requested)
        return list( seen_twice )
    
    @staticmethod
    def Find_Duplicates(fields_data,field_name,strType,usesForeignKey):
        strCombinedErrorMessage = None
        field_names = []
        for field_data in fields_data:
            str_data = field_data[field_name]
            if usesForeignKey == True:
                field_names.append(str_data.id)
            else:
                field_names.append(str_data)
        field_dupes = ValidationUtils.list_duplicates(field_names)
        if field_dupes is not None:
                if len(field_dupes) > 0:
                    strErrorMessage = '[' + ','.join(map(str, field_dupes)) + '].'                    
                    strCombinedErrorMessage =  "Following duplicate " + field_name + " found " + strErrorMessage + \
                                                 " Duplicate " + field_name + " not allowed within " + strType
        return strCombinedErrorMessage
    

    @staticmethod    
    def IsValidField(riskfield_data):
        strErrorMessage = None

        # Check if 
        if(riskfield_data is None):
            strErrorMessage =  "riskfield is not found. Post valid riskfield"

        if (riskfield_data.risk_type_field_enum and riskfield_data.risk_type_field_enum == "integer"):                    
            if (ValidationUtils.isanumber(riskfield_data.risk_field_value) == False):
                strErrorMessage =  riskfield_data.risk_type_field_name + " configured as " + riskfield_data.risk_type_field_enum + " This field must be an integer number."                                                        

        elif (riskfield_data.risk_type_field_enum and (riskfield_data.risk_type_field_enum == "number" or riskfield_data.risk_type_field_enum == "currency")):                     
            if (ValidationUtils.isanumber(riskfield_data.risk_field_value) == False):
                strErrorMessage =  riskfield_data.risk_type_field_name + " configured as " + riskfield_data.risk_type_field_enum + " This field must be an real number."                                                        

        elif riskfield_data.risk_type_field_enum and riskfield_data.risk_type_field_enum == "date":                     
            if (ValidationUtils.isadate(riskfield_data.risk_field_value) == False):
                strErrorMessage =  riskfield_data.risk_type_field_name + " configured as " + riskfield_data.risk_type_field_enum + " Enter date in MM/dd/yyyy format"                                                        

        elif riskfield_data.risk_type_field_enum and riskfield_data.risk_type_field_enum == "string":                     
            if (ValidationUtils.isastring(riskfield_data.risk_field_value) == False):
                strErrorMessage =  riskfield_data.risk_type_field_name + " configured as " + riskfield_data.risk_type_field_enum + " Enter valid string"                                                        

        return strErrorMessage
    @staticmethod    
    def IsValidInteger(riskfield_data):
        strErrorMessage = None
        if riskfield_data.risk_type_field_enum and riskfield_data.risk_type_field_enum == "integer":                    
            if (ValidationUtils.isadate(riskfield_data.risk_field_value) == False):
                strErrorMessage =  riskfield_data.risk_type_field_name + " configured as " + riskfield_data.risk_type_field_enum + " This field must be an integer number."                                                        
            return strErrorMessage
    @staticmethod
    def isanumber(inp):
        try:
            val = int(inp)
            return True
        except ValueError:
            try:
                val = float(inp)
                return True
            except ValueError:
                return False

    @staticmethod
    def isadate(inp):
        month,day,year = inp.split('/')
        isValidDate = True
        try :
            datetime.datetime(int(year),int(month),int(day))
        except ValueError :
            isValidDate = False
        return isValidDate

    
    @staticmethod
    def isastring(inp):
        isValidString = bool(inp and inp.strip())
        return isValidString

class RiskFieldValidator:
    def __init__(self, risk_type_field_enum):        
        self.risk_type_field_enum = risk_type_field_enum
        print('RiskFieldValidator init')

    def set_context(self, risk_type_field_enum):
        print(risk_type_field_enum)
        self.risk_type_field_enum = risk_type_field_enum

    def __call__(self, value):
        risk_field_value = value
        #serializer = self.serializer_field.parent
        #raw_start_date = serializer.initial_data[self.start_date_field]

        """ try:
            risk_type_field_enum = serializer.fields[self.risk_type_field_enum]
        except ValidationError:
            return  # if start_date is incorrect we will omit validating range """

        print('self.risk_type_field_enum')
        print(self.risk_type_field_enum)
        if self.risk_type_field_enum and self.risk_type_field_enum == "integer":
            if (isinstance(risk_field_value,int) == False):
                raise serializers.ValidationError('This field must be an integer number.') 
           

        