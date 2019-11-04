from import_export import resources
from riskapi.models import RiskType, RiskTypeField

class RiskTypeResource(resources.ModelResource):
    class Meta:
        model = RiskType
    
class RiskTypeFieldResource(resources.ModelResource):
    class Meta:
        model = RiskTypeField