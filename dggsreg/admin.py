#-*- coding:utf-8 -*-
from django.contrib import admin
from dggsreg.models import *
from skosxl.admin import *
from django.utils.translation import ugettext_lazy as _


    
class DGGSRegAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(DGGSRegAdmin, self).get_form(request, obj, **kwargs)

        form.base_fields['basepoly'].queryset = Concept.objects.filter(scheme__uri=BASEPOLYHEDRON_CODELIST)
        form.base_fields['refmodel'].queryset = Concept.objects.filter(scheme__uri=REFMODEL_CODELIST)
        form.base_fields['celltype'].queryset = Concept.objects.filter(scheme__uri=CELLTYPE_CODELIST)
        form.base_fields['tessellation_method'].queryset = Concept.objects.filter(scheme__uri=TESSELLATION_CODELIST)
        return form

class DGGSConformanceTestsAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        pass
 
admin.site.register(DGGSReg, DGGSRegAdmin)
admin.site.register(DGGSConformanceTests, DGGSRegAdmin)

