from enum import Enum
import json
import graphene
from riskapi.serializers import UserSerializer, RiskTypeKeySerializer, \
                                RiskKeySerializer, RiskTypeSerializer, \
                                RiskSerializer
from pocserver import adminschema
from rest_framework.test import APITestCase
# import pytest
# from py.test import raises

class JsonFileWriter(object):
    def __init__(self, fileName):        
        self.fileName = fileName

    def writeDictToFile(self, dictToWrite):
        f = open(self.fileName, "w")
        strErrorMessage = json.dumps(dictToWrite)
        f.write(strErrorMessage)
        f.close()

PostRequest_RiskTypesDict = {
    'Automobile': {
        'risk_type_name': 'Automobile',
        'risk_type_description': 'Type for Automobile Risk',
        'risktype_risktypefields': [
            {
                'risk_type_field_name': 'model',
                'risk_type_field_enum': 'text',
                'risk_type_field_description': 'Model of Automobile'
            },
            {
                'risk_type_field_name': 'doors',
                'risk_type_field_enum': 'integer',
                'risk_type_field_description': 'Number of doors'
            },
            {
                'risk_type_field_name': 'amount',
                'risk_type_field_enum': 'currency',
                'risk_type_field_description': 'Insurance Amount'
            },
            {
                'risk_type_field_name': 'issuedate',
                'risk_type_field_enum': 'date',
                'risk_type_field_description': 'License issued on date'
            }
        ]
    },
    'Home': {
        "risk_type_name": "Home",
        "risk_type_description": "Type for Home Risk",
        "risktype_risktypefields": [
            {
                "risk_type_field_name": "housenumber",
                "risk_type_field_enum": "text",
                "risk_type_field_description": "House number alloted by corporation"
            },
            {
                "risk_type_field_name": "floors",
                "risk_type_field_enum": "integer",
                "risk_type_field_description": "Number of floors"
            },
            {
                "risk_type_field_name": "sum",
                "risk_type_field_enum": "currency",
                "risk_type_field_description": "Sum Insurance Amount"
            },
            {
                "risk_type_field_name": "completion",
                "risk_type_field_enum": "date",
                "risk_type_field_description": "Construction completion date"
            }
        ]
    },
    'Having_DuplicateFieldName': {
            'risk_type_name': 'Automobile1',
            'risk_type_description': 'Type for Automobile Risk',
            'risktype_risktypefields': [
                {
                    'risk_type_field_name': 'model',
                    'risk_type_field_enum': 'text',
                    'risk_type_field_description': 'Model of Automobile'
                },
                {
                    'risk_type_field_name': 'model',
                    'risk_type_field_enum': 'integer',
                    'risk_type_field_description': 'Number of doors'
                },
                {
                    'risk_type_field_name': 'amount',
                    'risk_type_field_enum': 'currency',
                    'risk_type_field_description': 'Insurance Amount'
                },
                {
                    'risk_type_field_name': 'amount',
                    'risk_type_field_enum': 'date',
                    'risk_type_field_description': 'License issued on date(MM/dd/yyyy)'
                }
            ]
    }
}

PostResponse_RiskTypeDict = { 
   "all_risktypes" : [ 
      { 
         "id":"1",
         "risk_type_name":"Automobile",
         "risk_type_description":"Type for Automobile Risk",
         "risktype_risktypefields":[ 
            { 
               "id":"1",
               "risktype":"1",
               "risk_type_field_name":"model",
               "risk_type_field_enum":"text",
               "risk_type_field_description":"Model of Automobile"
            },
            { 
               "id":"2",
               "risktype":"1",
               "risk_type_field_name":"doors",
               "risk_type_field_enum":"integer",
               "risk_type_field_description":"Number of doors"
            },
            { 
               "id":"3",
               "risktype":"1",
               "risk_type_field_name":"amount",
               "risk_type_field_enum":"currency",
               "risk_type_field_description":"Insurance Amount"
            },
            { 
               "id":"4",
               "risktype":"1",
               "risk_type_field_name":"issuedate",
               "risk_type_field_enum":"date",
               "risk_type_field_description":"License issued on date"
            }
         ]
      },
      { 
         "id":"2",
         "risk_type_name":"Home",
         "risk_type_description":"Type for Home Risk",
         "risktype_risktypefields":[ 
            { 
               "id":"5",
               "risktype":"2",
               "risk_type_field_name":"housenumber",
               "risk_type_field_enum":"text",
               "risk_type_field_description":"House number alloted by corporation"
            },
            { 
               "id":"6",
               "risktype":"2",
               "risk_type_field_name":"floors",
               "risk_type_field_enum":"integer",
               "risk_type_field_description":"Number of floors"
            },
            { 
               "id":"7",
               "risktype":"2",
               "risk_type_field_name":"sum",
               "risk_type_field_enum":"currency",
               "risk_type_field_description":"Sum Insurance Amount"
            },
            { 
               "id":"8",
               "risktype":"2",
               "risk_type_field_name":"completion",
               "risk_type_field_enum":"date",
               "risk_type_field_description":"Construction completion date"
            }
         ]
      }
   ]
}

PostResponse_RiskTypeKeysDict = [ 
   { 
      "id":"1",
      "risk_type_name":"Automobile"
   },
   { 
      "id":"2",
      "risk_type_name":"Home"
   }
]

PostRequest_RisksDict = {
    'Automobile': {
        "risktype": 1,
        "risk_name": "Toyota 1",
        "risk_description": "Toyota 1 Risk policy",
        "risk_riskfields": [
            {
                "risktypefield": 1,
                "risk_field_value": "TYT1000"               
            },
            {
                "risktypefield": 2,
                "risk_field_value": "4"
            },
            {
                "risktypefield": 3,
                "risk_field_value": "1000.00"
            },
            {
                "risktypefield": 4,
                "risk_field_value": "11/01/2004"
            }
        ]
    },
    'Home': {
        "risktype": 2,
        "risk_name": "HillView",
        "risk_description": "Risk policy for HillView home",
        "risk_riskfields": [
            {
                "risktypefield": 5,
                "risk_field_value": "RL110107"                       
            },
            {
                "risktypefield": 6,
                "risk_field_value": "2"
            },
            {
                "risktypefield": 7,
                "risk_field_value": "10000.00" 
            },
            {
                "risktypefield": 8,
                "risk_field_value": "02/23/2001" 
            }
        ]
    },
    'Having_DuplicateFieldName': {
        "risktype": 1,
        "risk_name": "Toyota 2",
        "risk_description": "Toyota 1 Risk policy",
        "risk_riskfields": [
            {
                "risktypefield": 1,
                "risk_field_value": "TYT1000"
            },
            {
                "risktypefield": 1,
                "risk_field_value": "4"
            },
            {
                "risktypefield": 3,
                "risk_field_value": "1000.00"
            },
            {
                "risktypefield": 3,
                "risk_field_value": "11/01/2004"
            }
        ]
    },
    'Having_InvalidFieldValues': {
        "risktype": 1,
        "risk_name": "Toyota 2",
        "risk_description": "Toyota 1 Risk policy",
        "risk_riskfields": [
            {
                "risktypefield": 1,
                "risk_field_value": "TYT1000"
            },
            {
                "risktypefield": 2,
                "risk_field_value": "gggg"
            },
            {
                "risktypefield": 3,
                "risk_field_value": "1000.00"
            },
            {
                "risktypefield": 4,
                "risk_field_value": "jj34&&77"
            }
        ]
    }
}

PostResponse_RisksDict = { 
   "all_risks" : [
   {
      "id":"1",
      "risk_description":"Toyota 1 Risk policy",
      "risk_name":"Toyota 1",
      "risk_riskfields":[
         {
            "id":"1",
            "risk":"1",
            "risk_field_value":"TYT1000",
            "risk_type_field_name":"model",
            "risktypefield":"1"
         },
         {
            "id":"2",
            "risk":"1",
            "risk_field_value":"4",
            "risk_type_field_name":"doors",
            "risktypefield":"2"
         },
         {
            "id":"3",
            "risk":"1",
            "risk_field_value":"1000.00",
            "risk_type_field_name":"amount",
            "risktypefield":"3"
         },
         {
            "id":"4",
            "risk":"1",
            "risk_field_value":"11/01/2004",
            "risk_type_field_name":"issuedate",
            "risktypefield":"4"
         }
      ],
      "risk_type_name":"Automobile",
      "risktype":1
   },
   {
      "id":"2",
      "risk_description":"Risk policy for HillView home",
      "risk_name":"HillView",
      "risk_riskfields":[
         {
            "id":"5",
            "risk":"2",
            "risk_field_value":"RL110107",
            "risk_type_field_name":"housenumber",
            "risktypefield":"5"
         },
         {
            "id":"6",
            "risk":"2",
            "risk_field_value":"2",
            "risk_type_field_name":"floors",
            "risktypefield":"6"
         },
         {
            "id":"7",
            "risk":"2",
            "risk_field_value":"10000.00",
            "risk_type_field_name":"sum",
            "risktypefield":"7"
         },
         {
            "id":"8",
            "risk":"2",
            "risk_field_value":"02/23/2001",
            "risk_type_field_name":"completion",
            "risktypefield":"8"
         }
      ],
      "risk_type_name":"Home",
      "risktype":2
   }
]
}

AutomobileResponse = {
   "id":"1",
   "risk_description":"Toyota 1 Risk policy",
   "risk_name":"Toyota 1",
   "risk_riskfields":[
      {
         "id":"1",
         "risk":"1",
         "risk_field_value":"TYT1000",
         "risk_type_field_enum":"text",
         "risk_type_field_name":"model",
         "risktypefield":"1"
      },
      {
         "id":"2",
         "risk":"1",
         "risk_field_value":"4",
         "risk_type_field_enum":"integer",
         "risk_type_field_name":"doors",
         "risktypefield":"2"
      },
      {
         "id":"3",
         "risk":"1",
         "risk_field_value":"1000.00",
         "risk_type_field_enum":"currency",
         "risk_type_field_name":"amount",
         "risktypefield":"3"
      },
      {
         "id":"4",
         "risk":"1",
         "risk_field_value":"11/01/2004",
         "risk_type_field_enum":"date",
         "risk_type_field_name":"issuedate",
         "risktypefield":"4"
      }
   ],
   "risk_type_name":"Automobile",
   "risktype":1
}


RiskTypeKeysArray = [
    {
        "id": 1,
        "risk_type_name": "Automobile"
    },
    {
        "id": 2,
        "risk_type_name": "Home"
    }
]

RiskKeysArray = [
    {
        "id": 1,
        "risk_name": "Toyota 1"
    },
    {
        "id": 2,
        "risk_name": "HillView"
    }
]

AdminUserQueryResult = [
    {
        "password": "pbkdf2_sha256$100000$HX18m0pY5guH$kDdhbHL/6Dw+avdowDYTIP1HhHE8knLdSwYFolDIsJE=",
        "username": "mahesh.bodas",
        "email": "mahesh.bodas@gmail.com",
        "is_staff": True,
        "is_superuser": True,
        "is_active": True,
        "date_joined": "2018-11-21T10:03:27.146833Z"
    }
]

NonAdminUserQueryResult = [
    {
        "password": "pbkdf2_sha256$100000$WLtBTFMjr9NM$zhzbOrPIMejVBfA7LN9PM+hko/KvfyOYWjvtGDHUYd8=",
        "username": "editor",
        "email": "",
        "is_staff": False,
        "is_superuser": False,
        "is_active": True,
        "date_joined": "2018-11-29T19:06:58Z"
    }
]


class SetupTypes(Enum):
    RISKTYPE = 1
    RISK = 2


class SetupUser(Enum):
    ADMIN = 1
    NONADMIN = 2


class TestType:
    __payLoadKey = ""

    def __init__(self, payLoadKey):
        self.__payLoadKey = payLoadKey
    
    def getPayloadKey(self):
        return self.__payLoadKey

    def getPostRequest(self):
        pass

    def getPostResponse(self):
        pass


class TestRiskType(TestType):
    def __init__(self, payLoadKey):
        TestType.__init__(self, payLoadKey)

    def getPostRequest(self):
        if self.getPayloadKey() is 'All':
            allRiskTypePostRequests = []
            autoRiskType = PostRequest_RiskTypesDict['Automobile']
            allRiskTypePostRequests.append(autoRiskType)
            homeRiskType = PostRequest_RiskTypesDict['Home']
            allRiskTypePostRequests.append(homeRiskType)
            return allRiskTypePostRequests
        else:
            return PostRequest_RiskTypesDict[self.getPayloadKey()]

    def getPostResponse(self):
        # return PostResponse_RiskTypeDict[self.getPayloadKey()]
        if self.getPayloadKey() is 'All':
            allRiskTypePostResponses = []
            allRiskTypePostResponses = PostResponse_RiskTypeDict
            return allRiskTypePostResponses
        elif self.getPayloadKey() is 'Automobile':
            return PostResponse_RiskTypeDict['all_risktypes'][0]

        elif self.getPayloadKey() is 'Home':
            return PostResponse_RiskTypeDict['all_risktypes'][1]

    def getRiskTypeKeysResponse(self):
        return PostResponse_RiskTypeKeysDict


#
class TestRisk(TestType):
    def __init__(self, payLoadKey):
        TestType.__init__(self, payLoadKey)

    def getPostRequest(self):
        # return PostRequest_RisksDict[self.getPayloadKey()]
        if self.getPayloadKey() is 'All':
            allRiskPostRequests = []
            autoRisk = PostRequest_RisksDict['Automobile']
            allRiskPostRequests.append(autoRisk)
            homeRisk = PostRequest_RiskTypesDict['Home']
            allRiskPostRequests.append(homeRisk)
            return allRiskPostRequests
        else:
            return PostRequest_RisksDict[self.getPayloadKey()]

    def getPostResponse(self):
        # return PostResponse_RisksDict[self.getPayloadKey()]
        if self.getPayloadKey() is 'All':
            allRiskPostResponses = []
            allRiskPostResponses = PostResponse_RisksDict
            return allRiskPostResponses

        elif self.getPayloadKey() is 'Automobile':
            return PostResponse_RisksDict['all_risks'][0]

        elif self.getPayloadKey() is 'Home':
            return PostResponse_RisksDict['all_risks'][1]
        pass

class AdminQueryRiskTypeTests(APITestCase):
    def setUp(self):
        oTestRiskType = TestRiskType("Automobile")
        serializer = RiskTypeSerializer(data=oTestRiskType.getPostRequest())
        serializer.is_valid(raise_exception=True)
        serializer.save()

        oTestRiskType = TestRiskType("Home")
        serializer = RiskTypeSerializer(data=oTestRiskType.getPostRequest())
        serializer.is_valid(raise_exception=True)
        serializer.save()


    def test_should_query_all_risktype(self):
        testschema = graphene.Schema(query=adminschema.AdminQuery, auto_camelcase=False,)
        all_risktypes_query = """
            query {
                all_risktypes{
                    id,	
                    risk_type_name,
                    risk_type_description,
                    risktype_risktypefields {
                        id,
                        risktype,
                        risk_type_field_name,
                        risk_type_field_enum,
                        risk_type_field_description                        
                    }
                }
            }
        """       
        
        response = testschema.execute(all_risktypes_query)        
        # content = json.loads(response.data)
        # print(response.data)
        json_response = json.dumps(dict(response.data), sort_keys=True)        
        # print(json_response)
        # print("============================")
        # print(result.errors)
        # print(result)
        # oJsonFileWriter = JsonFileWriter("demofile.txt")
        # oJsonFileWriter.writeDictToFile(json.dumps(content))
        oTestRiskType = TestRiskType("All")
        # print(oTestRiskType.getPostResponse())
        all_risks_response_to_expect = oTestRiskType.getPostResponse()
        all_risks_response_to_expect = all_risks_response_to_expect['all_risktypes']
        a, b = json_response, json.dumps(oTestRiskType.getPostResponse(), sort_keys=True)
        assert a == b
        assert not response.errors    
    
    def test_should_query_SingleRisktype(self):
        testschema = graphene.Schema(query=adminschema.AdminQuery, auto_camelcase=False,)
        getSingleRisktype = """
            query getSingleRisktype($risktypeid:Int!) {
                risktypeobj:risktype(id:$risktypeid){
                    id,	
                    risk_type_name,
                    risk_type_description,
                    risktype_risktypefields {
                    id,
                    risktype,
                    risk_type_field_name,
                    risk_type_field_enum,
                    risk_type_field_description
                    }
                }
            }
        """       
        
        response = testschema.execute(getSingleRisktype, variables={'risktypeid': 1})                      
        json_response = json.dumps(response.data['risktypeobj'], sort_keys=True)        
        # print(json_response)
        # print(json_response)
        # print("============================")
        # print(response.errors)
        # print(result)
        # oJsonFileWriter = JsonFileWriter("demofile.txt")
        # oJsonFileWriter.writeDictToFile(json.dumps(content))
        oTestRiskType = TestRiskType("Automobile")        
        a, b = json_response, json.dumps(oTestRiskType.getPostResponse(), sort_keys=True)
        assert a == b
        assert not response.errors    


    def test_should_query_SingleRisktypeByName(self):
        testschema = graphene.Schema(query=adminschema.AdminQuery, auto_camelcase=False,)
        getSingleRisktype = """
            query getSingleRisktype($risktypename:String!) {
                risktypeobj:risktype(risk_type_name:$risktypename){
                    id,	
                    risk_type_name,
                    risk_type_description,
                    risktype_risktypefields {
                    id,
                    risktype,
                    risk_type_field_name,
                    risk_type_field_enum,
                    risk_type_field_description
                    }
                }
            }
        """       
        strRiskTypeName = "Home"
        response = testschema.execute(getSingleRisktype, variables={'risktypename': strRiskTypeName})                      
        # print(response.errors)
        json_response = json.dumps(response.data['risktypeobj'], sort_keys=True)        
        # print(json_response)
        
        oTestRiskType = TestRiskType(strRiskTypeName)        
        a, b = json_response, json.dumps(oTestRiskType.getPostResponse(), sort_keys=True)
        assert a == b
        assert not response.errors    

    def test_should_query_all_risktype_keys(self):
        testschema = graphene.Schema(query=adminschema.AdminQuery, auto_camelcase=False,)
        getRiskTypeKeys = """            
            query getAllRiskTypeKeys {
                risktypekeys:all_risktypes  {
                    id,     
                    risk_type_name
                }
            }
        """       
        response = testschema.execute(getRiskTypeKeys)                      
        # print(response.errors)
        json_response = json.dumps(response.data['risktypekeys'], sort_keys=True)        
        # print(json_response)
        
        oTestRiskType = TestRiskType("All")        
        a, b = json_response, json.dumps(oTestRiskType.getRiskTypeKeysResponse(), sort_keys=True)
        assert a == b
        assert not response.errors    


class AdminMutationRiskTypeTests(APITestCase):
       
    def test_should_create_Risktype(self):
        riskTypeInput = { 
                "risk_type_name":"Home",
                "risk_type_description":"Type for Home Risk",
                "risktype_risktypefields":[ 
                    { 
                        "risk_type_field_name":"housenumber",
                        "risk_type_field_enum":"text",
                        "risk_type_field_description":"House number alloted by corporation"
                    },
                    { 
                        "risk_type_field_name":"floors",
                        "risk_type_field_enum":"integer",
                        "risk_type_field_description":"Number of floors"
                    },
                    { 
                        "risk_type_field_name":"sum",
                        "risk_type_field_enum":"currency",
                        "risk_type_field_description":"Sum Insurance Amount"
                    },
                    { 
                        "risk_type_field_name":"completion",
                        "risk_type_field_enum":"date",
                        "risk_type_field_description":"Construction completion date"
                    }
                ]
        }
        testschema = graphene.Schema(mutation=adminschema.AdminMutation, auto_camelcase=False,)
        createRiskType = """
            mutation createRiskType($riskTypeInput:RiskTypeInput!) {
                create_risktype(input:$riskTypeInput) {
                    ok,
                    risktype{
                        risk_type_name,
                        risk_type_description,
                        risktype_risktypefields {
                        risk_type_field_name,
                        risk_type_field_enum,
                        risk_type_field_description
                        }
                    } 		
                }
            }
        """       
        
        response = testschema.execute(createRiskType, variables={'riskTypeInput': riskTypeInput})                      
        json_response = json.dumps(response.data['create_risktype']['risktype'])        
        oTestRiskType = TestRiskType("Home")  
        a, b = json_response, json.dumps(oTestRiskType.getPostRequest())
        assert a == b
        assert not response.errors    


class AdminQueryRiskTests(APITestCase):
    def setUp(self):
        oTestRiskType = TestRiskType("Automobile")
        serializer = RiskTypeSerializer(data=oTestRiskType.getPostRequest())
        serializer.is_valid(raise_exception=True)
        serializer.save()

        oTestRiskType = TestRiskType("Home")
        serializer = RiskTypeSerializer(data=oTestRiskType.getPostRequest())
        serializer.is_valid(raise_exception=True)
        serializer.save()

        oTestRisk = TestRisk("Automobile")
        serializer = RiskSerializer(data=oTestRisk.getPostRequest())
        serializer.is_valid(raise_exception=True)
        serializer.save()

        oTestRisk = TestRisk("Home")
        serializer = RiskSerializer(data=oTestRisk.getPostRequest())
        serializer.is_valid(raise_exception=True)
        serializer.save()



    def test_should_query_all_risk(self):
        testschema = graphene.Schema(query=adminschema.AdminQuery, auto_camelcase=False,)
        all_risks_query = """
            query {
                all_risks {
                    id,     
                    risktype,
                    risk_type_name,    
                    risk_name,    
                    risk_description,    
                    risk_riskfields {
                        id,    
                        risktypefield,
                        risk,        
                        risk_field_value,
                        risk_type_field_name
                    }    
                }
            }
        """       
        
        response = testschema.execute(all_risks_query)                     
        json_response = json.dumps(dict(response.data), sort_keys=True)         
        # print(json_response)
        json_response = json_response.strip()      
        # # print("============After=======================")
        # # print(json_response)
        oTestRisk = TestRisk("All")
        # print("===================================")
        # print(oTestRisk.getPostResponse())
        a, b = json_response, json.dumps(oTestRisk.getPostResponse(), sort_keys=True)
        assert a == b
        assert not response.errors    

    def test_should_query_SingleRisk(self):
        testschema = graphene.Schema(query=adminschema.AdminQuery, auto_camelcase=False,)
        getSingleRisk = """
            query getSingleRisk($riskid:Int!) {
                riskinstance:risk(id:$riskid) {
                    id,     
                    risktype,
                    risk_type_name,    
                    risk_name,    
                    risk_description,    
                    risk_riskfields {
                        id,    
                        risktypefield,
                        risk,  
                        risk_type_field_enum,  
                        risk_field_value,
                        risk_type_field_name
                    }    
                }
            }
        """       
        
        response = testschema.execute(getSingleRisk, variables={'riskid': 1})                                      
        json_response = json.dumps(dict(response.data['riskinstance']), sort_keys=True)                 
        # print(json_response)   
        # print("=================Strip==============")
        # json_response_strip = json_response.strip()   
        # print(json_response_strip)   
        # # print("============After=======================")
        # # print(json_response)
        # print(AutomobileResponse)
        a, b = json_response, json.dumps(AutomobileResponse, sort_keys=True)
        assert a == b
        assert not response.errors       

    def test_should_query_SingleRiskByName(self):
        testschema = graphene.Schema(query=adminschema.AdminQuery, auto_camelcase=False,)
        getSingleRisk = """
            query getSingleRisk($riskname:String!) {
                riskinstance:risk(risk_name:$riskname) {
                    id,     
                    risktype,
                    risk_type_name,    
                    risk_name,    
                    risk_description,    
                    risk_riskfields {
                        id,    
                        risktypefield,
                        risk,  
                        risk_type_field_enum,  
                        risk_field_value,
                        risk_type_field_name
                    }    
                }
            }
        """       
        strRiskName = "Toyota 1"
        response = testschema.execute(getSingleRisk, variables={'riskname': strRiskName})                      
        # print(response.errors)
        json_response = json.dumps(response.data['riskinstance'], sort_keys=True)        
        # print(json_response)
        
        a, b = json_response, json.dumps(AutomobileResponse, sort_keys=True)
        assert a == b
        assert not response.errors     

    def test_should_query_GetAllRisksByRisktype(self):
        testschema = graphene.Schema(query=adminschema.AdminQuery, auto_camelcase=False,)
        getSingleRisk = """
            query getAllRisksByRisktype($risktypeid:Int!) {
                riskinstances:all_risks(risktype:$risktypeid){
                    id,     
                    risktype,
                    risk_type_name,    
                    risk_name,    
                    risk_description,    
                    risk_riskfields {
                    id,    
                    risktypefield,
                    risk,        
                    risk_field_value,
                    risk_type_field_name
                    }    
                }
            }
        """       
        risktypeid = 1
        response = testschema.execute(getSingleRisk, variables={'risktypeid': risktypeid})                      
        assert not response.errors     

    def test_should_query_all_risk_keys(self):
        testschema = graphene.Schema(query=adminschema.AdminQuery, auto_camelcase=False,)
        getRiskKeys = """            
            query {
                riskkeys:all_risks  {
                    id,     
                    risk_name        
                }
            }
        """       
        response = testschema.execute(getRiskKeys)                      
        assert not response.errors