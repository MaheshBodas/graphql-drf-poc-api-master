# from django.contrib import admin
# from .models import RiskType, RiskTypeField, Risk, RiskField
# # https://gist.github.com/nimasmi/12b3200c3e1399123da6

# admin.site.register(RiskType)
# admin.site.register(riskapi,RiskType)
# admin.site.register(riskapi,RiskField)
# admin.site.register(riskapi,Risk)



from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import RiskType, RiskTypeField, Risk, RiskField

@admin.register(RiskType)
class RiskTypeAdmin(ImportExportModelAdmin):
    pass

@admin.register(RiskTypeField)
class RiskTypeFieldAdmin(ImportExportModelAdmin):
    pass

@admin.register(Risk)
class RiskAdmin(ImportExportModelAdmin):
    pass

@admin.register(RiskField)
class RiskFieldAdmin(ImportExportModelAdmin):
    pass