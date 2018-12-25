import datetime
""" from rest_framework.serializers import ValidationError
from .utils import * """


class ValidationUtils:
    @staticmethod
    def list_duplicates(seq):
        seen = set()
        seen_add = seen.add
        # adds all elements it doesn't know yet to seen and 
        # all other to seen_twice
        seen_twice = set(x for x in seq if x in seen or seen_add(x))
        # turn the set into a list (as requested)
        return list(seen_twice)

    @staticmethod
    def Find_Duplicates(fields_data, field_name, strType, usesForeignKey):
        strCombinedErrorMessage = None
        field_names = []
        for field_data in fields_data:
            str_data = field_data[field_name]
            if usesForeignKey is True:
                field_names.append(str_data.id)
            else:
                field_names.append(str_data)
        field_dupes = ValidationUtils.list_duplicates(field_names)
        if field_dupes is not None:
            if len(field_dupes) > 0:
                strErrorMessage = '[' + ','.join(map(str, field_dupes)) + '].'
                strCombinedErrorMessage = "Following duplicate " + field_name \
                                          + " found " + strErrorMessage + \
                                          " Duplicate " + field_name + \
                                          " not allowed within " + strType
        return strCombinedErrorMessage

    @staticmethod
    def IsValidField(oRiskFieldData):
        strErrorMessage = None

        # Check if
        if(oRiskFieldData is None):
            strErrorMessage = "riskfield is not found. Post valid riskfield"
        # print("In ValidationUtil IsValidField")
        # print(oRiskFieldData)
        if oRiskFieldData.risk_type_field_enum == "integer":
            bIsInteger = ValidationUtils.isanumber(
                        oRiskFieldData.risk_field_value)
            if bIsInteger is False:
                strErrorMessage = oRiskFieldData.risk_type_field_name + \
                                  " configured as " + \
                                  oRiskFieldData.risk_type_field_enum + \
                                  " This field must be valid integer."

        elif (oRiskFieldData.risk_type_field_enum == "number" or
              oRiskFieldData.risk_type_field_enum == "currency"):
            bIsNumber = ValidationUtils.isanumber(
                         oRiskFieldData.risk_field_value)
            if bIsNumber is False:
                strErrorMessage = oRiskFieldData.risk_type_field_name + \
                                 " configured as " + \
                                 oRiskFieldData.risk_type_field_enum + \
                                 " This field must be an real number."

        elif oRiskFieldData.risk_type_field_enum == "date":
            bIsDate = ValidationUtils.isadate(
                        oRiskFieldData.risk_field_value)
            if bIsDate is False:
                strErrorMessage = oRiskFieldData.risk_type_field_name + \
                 " configured as " + \
                 oRiskFieldData.risk_type_field_enum + \
                 " Enter date in MM/dd/yyyy format"

        elif oRiskFieldData.risk_type_field_enum == "string":
            bIsString = ValidationUtils.isastring(
                          oRiskFieldData.risk_field_value)
            if bIsString is False:
                strErrorMessage = oRiskFieldData.risk_type_field_name + \
                  " configured as " + \
                  oRiskFieldData.risk_type_field_enum + \
                  " Enter valid string"
        # print(strErrorMessage)
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
        try:
            month, day, year = inp.split('/')
            isValidDate = True
            datetime.datetime(int(year), int(month), int(day))
        except ValueError:
            isValidDate = False
        return isValidDate

    @staticmethod
    def isastring(inp):
        isValidString = bool(inp and inp.strip())
        return isValidString
