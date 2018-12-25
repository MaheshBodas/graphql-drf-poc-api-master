from enum import Enum
from django.contrib.auth.models import User
from riskapi.models import RiskType, Risk
from riskapi.serializers import UserSerializer, RiskTypeKeySerializer, \
                                RiskKeySerializer, RiskTypeSerializer, \
                                RiskSerializer
from riskapi.views import *
from rest_framework import status
from rest_framework.test import APITestCase
from django.test import TransactionTestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient
from rest_framework.exceptions import APIException
import json
# Use following post
# https://scotch.io/tutorials/build-a-rest-api-with-django-a-test-driven-approach-part-2#refactoring-our-tests

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
                'risk_type_field_description': 'License issued on date(MM/dd/yyyy)'
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
    'Automobile': {
                'id': 1,
                'risk_type_name': 'Automobile',
                'risk_type_description': 'Type for Automobile Risk',
                'risktype_risktypefields': [
                    {
                        'id': 1,
                        'risktype': 1,
                        'risk_type_field_name': 'model',
                        'risk_type_field_enum': 'text',
                        'risk_type_field_description': 'Model of Automobile'
                    },
                    {
                        'id': 2,
                        'risktype': 1,
                        'risk_type_field_name': 'doors',
                        'risk_type_field_enum': 'integer',
                        'risk_type_field_description': 'Number of doors'
                    },
                    {
                        'id': 3,
                        'risktype': 1,
                        'risk_type_field_name': 'amount',
                        'risk_type_field_enum': 'currency',
                        'risk_type_field_description': 'Insurance Amount'
                    },
                    {
                        'id': 4,
                        'risktype': 1,
                        'risk_type_field_name': 'issuedate',
                        'risk_type_field_enum': 'date',
                        'risk_type_field_description': 'License issued on date(MM/dd/yyyy)'
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
    'Having_DuplicateRiskTypeName': {
        'risk_type_name': ['risk_type_name must be unique']        
    },
    'Having_DuplicateFieldName': {
        "non_field_errors": ["Following duplicate risk_type_field_name found [model, amount]. Duplicate risk_type_field_name not allowed within RiskType"]
        }

}

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
    'Automobile': {
        "id": 1,
        "risktype": 1,
        "risk_type_name": "Automobile",
        "risk_name": "Toyota 1",
        "risk_description": "Toyota 1 Risk policy",
        "risk_riskfields": [
            {
                "id": 1,
                "risktypefield": 1,
                "risk": 1,
                "risk_type_field_name": "model",
                "risk_type_field_enum": "text",
                "risk_field_value": "TYT1000"
            },
            {
                "id": 2,
                "risktypefield": 2,
                "risk": 1,
                "risk_type_field_name": "doors",
                "risk_type_field_enum": "integer",
                "risk_field_value": "4"
            },
            {
                "id": 3,
                "risktypefield": 3,
                "risk": 1,
                "risk_type_field_name": "amount",
                "risk_type_field_enum": "currency",
                "risk_field_value": "1000.00"
            },
            {
                "id": 4,
                "risktypefield": 4,
                "risk": 1,
                "risk_type_field_name": "issuedate",
                "risk_type_field_enum": "date",
                "risk_field_value": "11/01/2004"
            }
        ]
    },
    'Home': {
        "id": 2,
        "risktype": 2,
        "risk_type_name": "Home",
        "risk_name": "HillView",
        "risk_description": "Risk policy for HillView home",
        "risk_riskfields": [
            {
                "id": 5,
                "risktypefield": 5,
                "risk": 2,
                "risk_type_field_name": "housenumber",
                "risk_type_field_enum": "text",
                "risk_field_value": "RL110107"
            },
            {
                "id": 6,
                "risktypefield": 6,
                "risk": 2,
                "risk_type_field_name": "floors",
                "risk_type_field_enum": "integer",
                "risk_field_value": "2"
            },
            {
                "id": 7,
                "risktypefield": 7,
                "risk": 2,
                "risk_type_field_name": "sum",
                "risk_type_field_enum": "currency",
                "risk_field_value": "10000.00"
            },
            {
                "id": 8,
                "risktypefield": 8,
                "risk": 2,
                "risk_type_field_name": "completion",
                "risk_type_field_enum": "date",
                "risk_field_value": "02/23/2001"
            }
        ]
    },
    'Having_DuplicateRiskName': {
        'risk_type_name': ['risk_type_name must be unique']
    },
    'Having_DuplicateFieldName': {
        'non_field_errors': ['Following duplicate risktypefield found [1,3]. Duplicate risktypefield not allowed within Risk']
    },
    'Having_InvalidFieldValues': {
        "non_field_errors": ["doors configured as integer This field must be valid integer.issuedate configured as date Enter date in MM/dd/yyyy format"]
    }
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
            autoRiskType = PostResponse_RiskTypeDict['Automobile']
            allRiskTypePostResponses.append(autoRiskType)
            homeRiskType = PostResponse_RiskTypeDict['Home']
            allRiskTypePostResponses.append(homeRiskType)
            return allRiskTypePostResponses
        else:
            return PostResponse_RiskTypeDict[self.getPayloadKey()]


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
            autoRisk = PostResponse_RisksDict['Automobile']
            allRiskPostResponses.append(autoRisk)
            homeRisk = PostResponse_RiskTypeDict['Home']
            allRiskPostResponses.append(homeRisk)
            return allRiskPostResponses
        else:
            return PostResponse_RisksDict[self.getPayloadKey()]
        pass


class SetUserHelper(object):
    def __init__(self, setupUser):        
        self.setupUser = setupUser

    def getUserPassword(self):
        if self.setupUser is SetupUser.ADMIN:
            return 'mahesh.bodas', "mypassword"
        elif self.setupUser is SetupUser.NONADMIN:
            return 'editor', "urpassword"

    def getUserPasswordEmail(self):
        if self.setupUser is SetupUser.ADMIN:
            return 'mahesh.bodas', "mypassword", 'myemail@test.com'
        elif self.setupUser is SetupUser.NONADMIN:
            return 'editor', "urpassword", 'myeditor@test.com'


class JsonFileWriter(object):
    def __init__(self, fileName):        
        self.fileName = fileName

    def writeDictToFile(self, dictToWrite):
        f = open(self.fileName, "w")
        strErrorMessage = json.dumps(dictToWrite)
        f.write(strErrorMessage)
        f.close()


class RiskApiBaseTests:
    def __init__(self):
        self.userHelper = None
        self.user = None
        self.client = None
        self.response = None
        self.postrequest = None
        self.postresponsetoexpect = None

    def setUserHelper(self, userHelper):
        self.userHelper = userHelper

    def setUser(self, user):
        self.user = user

    def setClient(self, client):
        self.client = client

    def setResponse(self, response):
        self.response = response

    def setPostRequest(self, postrequest):
        self.postrequest = postrequest

    def setPostResponseToExpect(self, postresponsetoexpect):
        self.postresponsetoexpect = postresponsetoexpect


class RiskApiTestBuilder:
    def getUserHelper(self):
        pass
    
    def getUser(self):
        pass

    def getClient(self, client):
        pass

    def getPostRequest():
        pass

    def getPostResponse(self, response):
        pass

    def getPostResponseToExpect(self, response):
        pass


class AdminUserRiskTypeTestBuilder(RiskApiTestBuilder):
    def getUserHelper(self):
        userHelper = SetUserHelper(SetupUser.ADMIN)
        return userHelper

    def getUser(self, userHelper):     
        userName, passWord, eMail = userHelper.getUserPasswordEmail()        
        my_admin = User.objects.create_superuser(
            userName, eMail, passWord)
        user = User.objects.get(username=my_admin)
        return user

    def getClient(self, userHelper):
        userName, passWord = userHelper.getUserPassword()  
        client = APIClient()
        client.login(username=userName, password=passWord)
        return client

    def getPostRequest(self):
        oTestRiskType = TestRiskType('Automobile')
        oPostRequestObj = oTestRiskType.getPostRequest()
        return oPostRequestObj

    def getPostResponse(self, client):
        oTestRiskType = TestRiskType('Automobile')
        oPostRequestObj = oTestRiskType.getPostRequest()
        response = client.post('/risktypes/', oPostRequestObj, format='json')
        return response
    
    def getPostResponseToExpect(self, client):
        oTestRiskType = TestRiskType('Automobile')
        oPostRequestObj = oTestRiskType.getPostResponse()
        return oPostRequestObj


class AdminUserRiskTestBuilder(RiskApiTestBuilder):
    def getUserHelper(self):
        userHelper = SetUserHelper(SetupUser.ADMIN)
        return userHelper

    def getUser(self, userHelper):     
        userName, passWord, eMail = userHelper.getUserPasswordEmail()        
        my_admin = User.objects.create_superuser(
            userName, eMail, passWord)
        user = User.objects.get(username=my_admin)

        # Lets also add non-admin user
        nonAdminUserHelper = SetUserHelper(SetupUser.NONADMIN)
        userName, passWord, eMail = nonAdminUserHelper.getUserPasswordEmail()        
        User.objects.create_user(
            userName, eMail, passWord)

        return user

    def getClient(self, userHelper):
        userName, passWord = userHelper.getUserPassword()
        client = APIClient()
        client.login(username=userName, password=passWord)
        return client

    def getPostRequest(self):
        oTestRisk = TestRisk('Automobile')
        oPostRequestObj = oTestRisk.getPostRequest()
        return oPostRequestObj

    def getPostResponse(self, client):
        # First post RiskType
        oTestRiskType = TestRiskType('Automobile')
        oPostRiskTypeRequestObj = oTestRiskType.getPostRequest()
        client.post('/risktypes/', oPostRiskTypeRequestObj, format='json')

        # First post Risk
        oTestRisk = TestRisk('Automobile')
        oPostRiskRequestObj = oTestRisk.getPostRequest()
        # print('Posting Risk Request')
        # print(oPostRiskRequestObj)
        response = client.post('/risks/', oPostRiskRequestObj, format='json')
        # print('Posted Risk response')
        # print(response)
        return response
    
    def getPostResponseToExpect(self, client):
        oTestRisk = TestRisk('Automobile')
        oPostRequestObj = oTestRisk.getPostResponse()
        return oPostRequestObj


# Director
class Director:
    
    """ Controls the construction process.
    Director has a builder associated with him. Director then
    delegates building of the smaller parts to the builder and
    assembles them together.
    """

    __builder = None

    def setBuilder(self, builder):
        self.__builder = builder

    # The algorithm for assembling a Test Type
    def getTestType(self, TestTypeToBuild):

        # First goes the userHelper
        userHelper = self.__builder.getUserHelper()
        TestTypeToBuild.setUserHelper(userHelper)

        # First goes the user
        user = self.__builder.getUser(userHelper)
        TestTypeToBuild.setUser(user)

        # Then client
        client = self.__builder.getClient(userHelper)
        TestTypeToBuild.setClient(client)

        # Then Post Request
        postrequest = self.__builder.getPostRequest()
        TestTypeToBuild.setPostRequest(postrequest)

        # Then Post response
        response = self.__builder.getPostResponse(client)
        TestTypeToBuild.setResponse(response)

        # Then Post response to expect
        responseToExpect = self.__builder.getPostResponseToExpect(client)
        TestTypeToBuild.setPostResponseToExpect(responseToExpect)
        
        return TestTypeToBuild
#


class AdminUserRiskTypeTests(APITestCase, RiskApiBaseTests):
    def setUp(self):
        director = Director()
        director.setBuilder(AdminUserRiskTypeTestBuilder())
        director.getTestType(self)

    def test_post_risk_type(self):
        username, password = self.userHelper.getUserPassword()
        self.client.login(username=username, password=password)
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RiskType.objects.count(), 1)

    def test_get_risk_type(self):
        username, password = self.userHelper.getUserPassword()
        self.client.login(username=username, password=password)
        #
        risktypelist = RiskType.objects.get(id=1)
        response = self.client.get(
            '/risktypes/',
            kwargs={'pk': risktypelist.id}, format="json")        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertContains(response.data, self.oResponse_RiskType)
        # expected_response_json = json.dumps(self.oResponse_RiskType)
        self.assertTrue(response, self.postresponsetoexpect)

    def test_get_risk_type_by_name(self):
        username, password = self.userHelper.getUserPassword()
        self.client.login(username=username, password=password)        
        response = self.client.get('/risktypes/?risk_type_name=Automobile',
                                   format='json')
        # response = self.view(request)
        # print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertTrue(response, self.postresponsetoexpect)

    def test_get_all_risk_types(self):        
        # While setting AdminUserRiskTypeTests we have posted
        # one RiskType we will post one more to test retrieving
        # multiple RiskTypes
        username, password = self.userHelper.getUserPassword()
        self.client.login(username=username, password=password)
        oTestRiskType = TestRiskType('Home')
        oTestRiskType = oTestRiskType.getPostRequest()
        self.client.post('/risktypes/', oTestRiskType, format='json')
        oTestAllRiskType = TestRiskType('All')
        oAllRiskTypePostResponsesToExpect = oTestAllRiskType.getPostResponse()

        # risktypelist = RiskType.objects.All()
        response = self.client.get(
            '/risktypes/',
            format="json")        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertContains(response.data, self.oResponse_RiskType)
        # expected_response_json = json.dumps(self.oResponse_RiskType)
        self.assertTrue(response, oAllRiskTypePostResponsesToExpect)
    
    def test_get_all_risk_type_keys(self):        
        # While setting AdminUserRiskTypeTests we have posted
        # one RiskType we will post one more to test retrieving
        # multiple RiskTypes
        username, password = self.userHelper.getUserPassword()
        self.client.login(username=username, password=password)
        
        # risktypelist = RiskType.objects.All()
        response = self.client.get(
            '/risktypekeys/',
            format="json") 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertContains(response.data, self.oResponse_RiskType)
        # expected_response_json = json.dumps(self.oResponse_RiskType)
        oAllRiskTypekeysResponsesToExpect = RiskTypeKeysArray
        self.assertTrue(response, oAllRiskTypekeysResponsesToExpect)

    def test_can_get_user_details(self):        
        # While setting AdminUserRiskTypeTests we have posted
        # one RiskType we will post one more to test retrieving
        # multiple RiskTypes
        username, password = self.userHelper.getUserPassword()
        self.client.login(username=username, password=password)
        
        # risktypelist = RiskType.objects.All()
        response = self.client.get(
            '/users/?username=' + username,
            format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertContains(response.data, self.oResponse_RiskType)
        # expected_response_json = json.dumps(self.oResponse_RiskType)
        oAdminUserQueryResult = AdminUserQueryResult
        self.assertTrue(response, oAdminUserQueryResult)
    
    def test_cannot_post_duplicate_risktype(self):
        # oErrorMessage = {'risk_type_name': ['risk_type_name must be unique']}
        oTestRiskType = TestRiskType('Having_DuplicateRiskTypeName')
        oErrorMessage = oTestRiskType.getPostResponse()
        username, password = self.userHelper.getUserPassword()
        self.client.login(username=username, password=password)
        response = self.client.post('/risktypes/', self.postrequest,
                                    format='json')
        # print(response.data)

        self.assertTrue(response, oErrorMessage)        

    def test_cannot_post_risktype_with_duplicate_field_names(self):
        oTestRiskType = TestRiskType('Having_DuplicateFieldName')
        oRiskType_Duplicate_field_names = oTestRiskType.getPostRequest()
        oErrorMessage = oTestRiskType.getPostResponse()
        username, password = self.userHelper.getUserPassword()
        self.client.login(username=username, password=password)
        dup_response = self.client.post('/risktypes/',
                                        oRiskType_Duplicate_field_names,
                                        format='json')
        # oJsonFileWriter = JsonFileWriter("demofile.txt")
        # oJsonFileWriter.writeDictToFile(dup_response.data)
        self.assertTrue(dup_response, oErrorMessage)


# NonAdmin user RiskType test


class NonAdminUserRiskTypeTests(APITestCase, RiskApiBaseTests):
    def setUp(self):
        director = Director()
        director.setBuilder(AdminUserRiskTypeTestBuilder())
        director.getTestType(self)
        
    def test_nonadmin_cannot_get_risktypes(self):
            """Test that the api has user authorization."""         
            new_client = APIClient()
            oSetUserHelper = SetUserHelper(SetupUser.NONADMIN)          
            username, password = oSetUserHelper.getUserPassword()
            new_client.login(username=username, password=password)         
            res = new_client.get(
                '/risktypes/', kwargs={'pk': 1}, format="json")
            self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_nonadmin_cannot_post_risktypes(self):
            """Test that the api has user authorization."""
            new_client = APIClient()            
            oSetUserHelper = SetUserHelper(SetupUser.NONADMIN)          
            username, password = oSetUserHelper.getUserPassword()
            new_client.login(username=username, password=password)
                 
            res = new_client.post('/risktypes/',
                                  self.postrequest,
                                  format='json')
            # print(res.data)
            # print(res.status_code)
            self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    #
    def test_get_all_risk_type_keys(self):
        # self.client.login(username=username, password=password)
        new_client = APIClient()
        oSetUserHelper = SetUserHelper(SetupUser.NONADMIN)
        username, password = oSetUserHelper.getUserPassword()
        new_client.login(username=username, password=password)
        # risktypelist = RiskType.objects.All()
        response = new_client.get(
            '/risktypekeys/',
            format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertContains(response.data, self.oResponse_RiskType)
        # expected_response_json = json.dumps(self.oResponse_RiskType)
        oAllRiskTypekeysResponsesToExpect = RiskTypeKeysArray
        self.assertTrue(response, oAllRiskTypekeysResponsesToExpect)

    def test_can_get_user_details(self):        
        new_client = APIClient()
        oSetUserHelper = SetUserHelper(SetupUser.NONADMIN)
        username, password = oSetUserHelper.getUserPassword()
        new_client.login(username=username, password=password)
        
        # risktypelist = RiskType.objects.All()
        response = self.client.get(
            '/users/?username=' + username,
            format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertContains(response.data, self.oResponse_RiskType)
        # expected_response_json = json.dumps(self.oResponse_RiskType)
        oNonAdminUserQueryResult = NonAdminUserQueryResult
        self.assertTrue(response, oNonAdminUserQueryResult)


# Admin Risk test
class AdminUserRiskTests(APITestCase, RiskApiBaseTests):
    def setUp(self):
        director = Director()
        director.setBuilder(AdminUserRiskTestBuilder())
        director.getTestType(self)

    def test_post_risk(self):
        username, password = self.userHelper.getUserPassword()
        self.client.login(username=username, password=password)
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RiskType.objects.count(), 1)

    def test_get_risk(self):
        username, password = self.userHelper.getUserPassword()
        self.client.login(username=username, password=password)
        #
        risklist = Risk.objects.get(id=1)
        response = self.client.get(
            '/risks/',
            kwargs={'pk': risklist.id}, format="json")        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertContains(response.data, self.oResponse_RiskType)
        # expected_response_json = json.dumps(self.oResponse_RiskType)
        self.assertTrue(response, self.postresponsetoexpect)

    def test_get_risk_by_name(self):
        username, password = self.userHelper.getUserPassword()
        self.client.login(username=username, password=password)        
        response = self.client.get('/risks/?risk_name=Toyota 1',
                                   format='json')
        # response = self.view(request)
        # print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertTrue(response, self.postresponsetoexpect)

    def test_get_all_risk_types(self):
        
        # While setting AdminUserRiskTypeTests we have posted
        # one RiskType we will post one more to test retrieving
        # multiple RiskTypes
        username, password = self.userHelper.getUserPassword()
        self.client.login(username=username, password=password)
        oTestRisk = TestRisk('Home')
        oTestRisk = oTestRisk.getPostRequest()
        self.client.post('/risks/', oTestRisk, format='json')
        oTestAllRisk = TestRisk('All')
        oAllRiskPostResponsesToExpect = oTestAllRisk.getPostResponse()

        # risktypelist = RiskType.objects.All()
        response = self.client.get(
            '/risktypes/',
            format="json")        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertContains(response.data, self.oResponse_RiskType)
        # expected_response_json = json.dumps(self.oResponse_RiskType)
        self.assertTrue(response, oAllRiskPostResponsesToExpect)

    def test_get_all_risk_keys(self):        
        # While setting AdminUserRiskTypeTests we have posted
        # one RiskType we will post one more to test retrieving
        # multiple RiskTypes
        username, password = self.userHelper.getUserPassword()
        self.client.login(username=username, password=password)
        
        # risktypelist = RiskType.objects.All()
        response = self.client.get(
            '/riskkeys/',
            format="json") 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertContains(response.data, self.oResponse_RiskType)
        # expected_response_json = json.dumps(self.oResponse_RiskType)
        oAllRiskkeysResponsesToExpect = RiskKeysArray
        self.assertTrue(response, oAllRiskkeysResponsesToExpect)

    def test_cannot_post_duplicate_risktype(self):
        # oErrorMessage = {'risk_type_name': ['risk_type_name must be unique']}
        oTestRisk = TestRisk('Having_DuplicateRiskName')
        oErrorMessage = oTestRisk.getPostResponse()
        username, password = self.userHelper.getUserPassword()
        self.client.login(username=username, password=password)
        response = self.client.post('/risks/', self.postrequest,
                                    format='json')
        # print(response.data)

        self.assertTrue(response, oErrorMessage)        

    def test_cannot_post_risktype_with_duplicate_field_names(self):
        oTestRisk = TestRisk('Having_DuplicateFieldName')
        oRisk_Duplicate_field_names = oTestRisk.getPostRequest()
        oErrorMessage = oTestRisk.getPostResponse()
        # print(oErrorMessage)
        username, password = self.userHelper.getUserPassword()
        self.client.login(username=username, password=password)
        dup_response = self.client.post('/risks/',
                                        oRisk_Duplicate_field_names,
                                        format='json')
        # oJsonFileWriter = JsonFileWriter("demofile.txt")
        # oJsonFileWriter.writeDictToFile(dup_response.data)
        self.assertTrue(dup_response, oErrorMessage)

    def test_cannot_post_risktype_with_invalid_field_values(self):
        oTestRisk = TestRisk('Having_InvalidFieldValues')
        oRisk_Invalid_field_values = oTestRisk.getPostRequest()
        oErrorMessage = oTestRisk.getPostResponse()
        # print(oErrorMessage)
        username, password = self.userHelper.getUserPassword()
        self.client.login(username=username, password=password)
        invalid_response = self.client.post('/risks/',
                                            oRisk_Invalid_field_values,
                                            format='json')
        # oJsonFileWriter = JsonFileWriter("demofile.txt")
        # oJsonFileWriter.writeDictToFile(invalid_response.data)
        self.assertTrue(invalid_response, oErrorMessage)


class NonAdminUserRiskTests(APITestCase, RiskApiBaseTests):
    def setUp(self):
        director = Director()
        director.setBuilder(AdminUserRiskTestBuilder())
        director.getTestType(self)

    def test_nonadmin_can_post_risk_type(self):
        new_client = APIClient()
        oSetUserHelper = SetUserHelper(SetupUser.NONADMIN)
        username, password = oSetUserHelper.getUserPassword()
        new_client.login(username=username, password=password)

        # Post RiskType using Admin user account
        oTestRiskType = TestRiskType('Home')
        oTestPostRiskType = oTestRiskType.getPostRequest()
        resRisk = self.client.post('/risktypes/', oTestPostRiskType, format='json')
        self.assertEqual(resRisk.status_code, status.HTTP_201_CREATED)
        # print('test_nonadmin_can_post_risk_type')
        # print(resRisk.data)

        oTestRisk = TestRisk('Home')
        oTestPostRisk = oTestRisk.getPostRequest()
        res = new_client.post('/risks/', oTestPostRisk, format='json')
        
        # print('test_nonadmin_can_post_risk')
        # print(res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(RiskType.objects.count(), 1)

    def test_nonadmin_can_get_risks(self):
        new_client = APIClient()
        oSetUserHelper = SetUserHelper(SetupUser.NONADMIN)      
        username, password = oSetUserHelper.getUserPassword()
        new_client.login(username=username, password=password)
        res = new_client.get(
            '/risks/', kwargs={'pk': 1}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # risklist = Risk.objects.get(id=1)
        # self.assertEqual(len(risklist), 1)
        self.assertEqual(Risk.objects.count(), 1)

    def test_get_all_risk_keys(self):
        # self.client.login(username=username, password=password)
        new_client = APIClient()
        oSetUserHelper = SetUserHelper(SetupUser.NONADMIN)
        username, password = oSetUserHelper.getUserPassword()
        new_client.login(username=username, password=password)
        response = new_client.get(
            '/riskkeys/',
            format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertContains(response.data, self.oResponse_RiskType)
        # expected_response_json = json.dumps(self.oResponse_RiskType)
        oAllRiskkeysResponsesToExpect = RiskTypeKeysArray
        self.assertTrue(response, oAllRiskkeysResponsesToExpect)
