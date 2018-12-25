from django.contrib.auth.models import User
from rest_framework import serializers
from .models import RiskType, RiskTypeField, Risk, RiskField
from .utils import RiskFieldData
from .validators import ValidationUtils

# Serializer type for User DRF authentication


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'username', 'email', 'is_staff',
                  'is_superuser', 'is_active', 'date_joined',)
        write_only_fields = ('password',)
        read_only_fields = ('is_staff', 'is_superuser',
                            'is_active', 'date_joined',)
        # Explicitly mark required fields
        required_fields = (
            'username',
            'password'
        )
        extra_kwargs = {field: {'required': True} for field in required_fields}

# Serializer type used for Lookups in select RiskType list in UI


class RiskTypeKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskType
        fields = ('id', 'risk_type_name')

# Serializer type used for Lookups in select risk list in UI


class RiskKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Risk
        fields = ('id', 'risk_name')

# Serializer type used for RiskTypeField nested in RiskType


class RiskTypeFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskTypeField
        # Have field for parent type RiskType name it risktype
        fields = ('id', 'risktype', 'risk_type_field_name',
                  'risk_type_field_enum', 'risk_type_field_description')
        # Explicitly mark required fields
        required_fields = (
            'risk_type_field_name',
            'risk_type_field_enum'
        )
        extra_kwargs = {field: {'required': True} for field in required_fields}

# Serializer type used for RiskType


class RiskTypeSerializer(serializers.ModelSerializer):
    createdby = serializers.ReadOnlyField(source='createdby.username')
    risktype_risktypefields = RiskTypeFieldSerializer(many=True)

    class Meta:
        model = RiskType
        fields = ('id', 'risk_type_name', 'risk_type_description',
                  'risktype_risktypefields', 'createdby')

    # Explicitly mark required fields
        required_fields = (
            'risk_type_name',
            'risktype_risktypefields'
        )
        extra_kwargs = {field: {'required': True} for field in required_fields}

    def get_validation_exclusions(self, *args, **kwargs):
        # exclude the author field as we supply it later on in the
        # corresponding view based on the http request
        exclusions = super(RiskTypeSerializer,
                           self).get_validation_exclusions(*args, **kwargs)
        return exclusions + ['createdby']

    def create(self, validated_data):
        # print('Calling ModelSerializer.validate()')
        # serializer = RiskTypeSerializer(data=data)
        # serializer.is_valid()
        # print(validated_data)
        risktypefields_data = validated_data.pop('risktype_risktypefields')

        risktypeobj = RiskType.objects.create(**validated_data)
        for risktypefield_data in risktypefields_data:
            RiskTypeField.objects.create(
                risktype=risktypeobj, **risktypefield_data)
        return risktypeobj

    #
    def validate(self, attrs):
        strCombinedErrorMessage = None
        # print("I am calling RiskType Validate")
        risktype_risktypefields_data = attrs['risktype_risktypefields']
        # print(risktype_risktypefields_data)
        if not risktype_risktypefields_data:
            strError = "risktypefields not defined for RiskType"
            # print(strError)
            raise serializers.ValidationError(strError)
        strCombinedErrorMessage = ValidationUtils.Find_Duplicates(
            risktype_risktypefields_data, 'risk_type_field_name', 'RiskType',
            False)
        if strCombinedErrorMessage is None:
            return attrs
        else:
            # print(strCombinedErrorMessage)
            raise serializers.ValidationError(strCombinedErrorMessage)
    #

# Serializer type used for riskfield nested in risk


class RiskFieldSerializer(serializers.ModelSerializer):
    risk_type_field_name = serializers.ReadOnlyField(
        source='risktypefield.risk_type_field_name')
    risk_type_field_enum = serializers.ReadOnlyField(
        source='risktypefield.risk_type_field_enum')
    risk_field_value = serializers.CharField(required=True)

    class Meta:
        model = RiskField
        fields = ('id', 'risktypefield', 'risk', 'risk_type_field_name',
                  'risk_type_field_enum', 'risk_field_value')

        # Explicitly mark required fields
        required_fields = (
            'risktypefield',
            'risk_field_value'
        )
        extra_kwargs = {field: {'required': True} for field in required_fields}

        def create(self, riskobj, validated_data):
            # Copy original posted data
            # Pop risktype
            # print('Writing risktypefield')
            risktypefield_qryobj = validated_data.pop('risktypefield')
            # print(risktypefield_qryobj.pk)
            risk_type_field_id = risktypefield_qryobj.pk
            qFilterSet = RiskTypeField.objects.filter(
                risktype__pk=riskobj.risk_type_id, id=risk_type_field_id)
            # print('qFilterSet count()')
            # print(qFilterSet.count())
            # risk_type_field_obj = qFilterSet.get(id=risk_type_field_id)
            self.risktypefield = qFilterSet.get(id=risk_type_field_id)

# Serializer type used for risk


class RiskSerializer(serializers.ModelSerializer):
    createdby = serializers.ReadOnlyField(source='createdby.username')
    risk_riskfields = RiskFieldSerializer(many=True)
    risk_type_name = serializers.ReadOnlyField(
        source='risktype.risk_type_name')

    class Meta:
        model = Risk
        fields = ('id', 'risktype', 'risk_type_name', 'risk_name',
                  'risk_description', 'risk_riskfields', 'createdby')
        # Explicitly mark required fields
        required_fields = (
            'risktype',
            'risk_name',
            'risk_riskfields'
        )
        extra_kwargs = {field: {'required': True} for field in required_fields}

    def get_validation_exclusions(self, *args, **kwargs):
        # exclude the author field as we supply it later on in the
        # corresponding view based on the http request
        exclusions = super(RiskSerializer, self).get_validation_exclusions(
            *args, **kwargs)
        return exclusions + ['createdby']

    def create(self, validated_data):
        # Copy original posted data
        # print(validated_data)
        # original_validated_data = validated_data.copy()        
        riskfields_data = validated_data.pop('risk_riskfields')
        # Pop risktype
        risktype_qryobj = validated_data.pop('risktype')
        # print('Writing primary key of risktype_qryobj')
        # print(riskfields_data)
        # print(risktype_qryobj.pk)
        # print(risktype_qryobj)
        risk_type_id = risktype_qryobj.pk
        #
        risk_type_obj = RiskType.objects.get(pk=risk_type_id)
        riskobj = Risk.objects.create(risktype=risk_type_obj, **validated_data)
        # risk_type_field_obj = risktypefield.objects.get(pk=1)
        for riskfield_data in riskfields_data:
            # print('Writing riskfield_data')
            # print(riskfield_data)
            # risk_type_field_obj.risktype = risk_type_id
            RiskField.objects.create(risk=riskobj, **riskfield_data)
            # riskfield.objects.create(risk=riskobj,risktypefield=risk_type_field_obj,**riskfield_data)
            # riskfield.objects.create(risk=riskobj,**riskfield_data)        
        return riskobj

    # Helper method to
    def GetRiskField(self, risk_type_id, riskfield_data):
        strErrorMessage = None
        oRiskFieldData = None
        # print('Validating riskfield_data')
        # print(riskfield_data)
        risktypefield_qryobj = riskfield_data["risktypefield"]
        risk_field_value = riskfield_data["risk_field_value"]
        # print(risktypefield_qryobj.pk)
        risk_type_field_id = risktypefield_qryobj.pk
        qFilterSet = RiskTypeField.objects.filter(
            risktype__pk=risk_type_id, id=risk_type_field_id)
        # qFilterSet = RiskTypeField.objects.filter(risktype__pk =1,
        # id=risk_type_field_id)
        # print('qFilterSet count()')
        # print(qFilterSet.count())
        # risk_type_field_obj = qFilterSet.get(id=risk_type_field_id)
        risktypefield_chk = qFilterSet.get(id=risk_type_field_id)
        if(risktypefield_chk is not None):
            # print(risktypefield_chk.risk_type_field_name)
            # print(risktypefield_chk.risk_type_field_enum)
            # print("risk_field_value is " + risk_field_value)
            oRiskFieldData = RiskFieldData(
                              risktypefield_chk.risk_type_field_name,
                              risktypefield_chk.risk_type_field_enum,
                              risk_field_value)
        else:
            oRiskFieldData = None
            strErrorMessage = "risktypefield id= " + risk_type_field_id + \
                              " is not found For risktype=" + risk_type_id + \
                              ". Enter valid id for Risktype"
        return oRiskFieldData, strErrorMessage

    def validate(self, attrs):
        # Validate Risk object
        strCombinedErrorMessage = None
        # print("I am calling risk Validate")
        risktype_qryobj = attrs['risktype']
        # print('Writing primary key of risktype_qryobj')
        # print(risktype_qryobj.pk)
        risk_type_id = risktype_qryobj.pk

        # Check primary key refers to valid RiskType
        qRiskTypeFilterSet = RiskType.objects.filter(id=risk_type_id)
        if(qRiskTypeFilterSet.count() != 1):
            strErrorMessage = "risktype id= " + risk_type_id + \
                " is not found. Enter valid id for Risktype"

        # Check user has posted valid riskfields nested object
        risk_riskfields_data = attrs['risk_riskfields']
        if not risk_riskfields_data:
            strError = "riskfields not defined for risk"
            # print(strError)
            raise serializers.ValidationError(strError)

        # Check for duplicate RiskFields
        strDuplicateRiskFields = None
        strDuplicateRiskFields = ValidationUtils.Find_Duplicates(
            risk_riskfields_data, 'risktypefield', 'Risk', True)
        if strDuplicateRiskFields:
            # print(strDuplicateRiskFields)
            raise serializers.ValidationError(strDuplicateRiskFields)

        # Check user has posted valid riskfield
        for riskfield_data in risk_riskfields_data:
            strErrorMessage = None
            # print("In validate risk_riskfields_data loop")
            # print(riskfield_data)
            oRiskFieldData, strErrorMessage = self.GetRiskField(
                risk_type_id, riskfield_data)
            if(strErrorMessage is None):
                strErrorMessage = ValidationUtils.IsValidField(oRiskFieldData)
            if(strErrorMessage is not None):
                if(strCombinedErrorMessage is None):
                    strCombinedErrorMessage = strErrorMessage
                else:
                    strCombinedErrorMessage = strCombinedErrorMessage +\
                                              strErrorMessage
        if strCombinedErrorMessage is None:
            return attrs
        else:
            # print(strCombinedErrorMessage)
            raise serializers.ValidationError(strCombinedErrorMessage)
