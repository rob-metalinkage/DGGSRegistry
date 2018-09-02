#-*- coding:utf-8 -*-
from django.contrib import admin
from dggsreg.models import *
from skosxl.admin import *
from django.utils.translation import ugettext_lazy as _

class DGGSConformanceTestsInline(admin.TabularInline):
    model=DGGSConformanceTest
    extra=1
    pass

class DGGSTessellationInline(admin.TabularInline):
    model=DGGSTessellation
    ordering = ('refinement_level',)
    extra=1
    pass
    
class DGGSRegAdmin(admin.ModelAdmin):
    inlines= [DGGSTessellationInline,
               DGGSConformanceTestsInline, ]
    def get_form(self, request, obj=None, **kwargs):
        form = super(DGGSRegAdmin, self).get_form(request, obj, **kwargs)

        form.base_fields['basepoly'].queryset = Concept.objects.filter(scheme__uri=BASEPOLYHEDRON_CODELIST)
        form.base_fields['refmodel'].queryset = Concept.objects.filter(scheme__uri=REFMODEL_CODELIST)
        #=======================================================================
        # form.base_fields['celltype1'].queryset = Concept.objects.filter(scheme__uri=CELLTYPE_CODELIST)
        #=======================================================================
        #=======================================================================
        # form.base_fields['celltype'].queryset = Concept.objects.filter(scheme__uri=CELLTYPE_CODELIST)
        # form.base_fields['celledgetype'].queryset = Concept.objects.filter(scheme__uri=EDGETYPE_CODELIST)
        #=======================================================================
        form.base_fields['tessellation_method'].queryset = Concept.objects.filter(scheme__uri=TESSELLATION_CODELIST)
        return form

class DGGSConformanceTestAdmin(admin.ModelAdmin):
    pass

class DGGSRequirementAdmin(admin.ModelAdmin):
    pass

class DGGSTessellationAdmin(admin.ModelAdmin):   
    def get_form(self, request, obj=None, **kwargs):
        form = super(DGGSTessellationAdmin, self).get_form(request, obj, **kwargs)
        
        form.base_fields['celltype'].queryset = Concept.objects.filter(scheme__uri=CELLTYPE_CODELIST)
        form.base_fields['celledgetype'].queryset = Concept.objects.filter(scheme__uri=EDGETYPE_CODELIST)
        return form    
        
admin.site.register(DGGSReg, DGGSRegAdmin)
admin.site.register(DGGSConformanceTest, DGGSConformanceTestAdmin)
admin.site.register(DGGSRequirement,DGGSRequirementAdmin)
admin.site.register(DGGSTessellation,DGGSTessellationAdmin)


