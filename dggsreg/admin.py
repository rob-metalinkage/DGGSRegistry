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
 
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(DGGSTessellationInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        field.widget.can_add_related = False
        if db_field.name == 'celltype':
            field.queryset = Concept.objects.filter(scheme__uri=CELLTYPE_CODELIST)
        elif db_field.name == 'celledgetype':
            field.queryset = Concept.objects.filter(scheme__uri=EDGETYPE_CODELIST)

        return field
 
    def get_formset(self, request, obj=None, **kwargs):
        """
        Override the formset function in order to remove the add and change buttons beside the foreign key pull-down
        menus in the inline.
        """
        formset = super(DGGSTessellationInline, self).get_formset(request, obj, **kwargs)
        form = formset.form
        for f in ['celltype','celledgetype']:
            widget = form.base_fields[f].widget
            widget.can_add_related = False
            widget.can_change_related = False
        
        return formset
    
    
class DGGSRegAdmin(admin.ModelAdmin):
    inlines= [DGGSTessellationInline,
               DGGSConformanceTestsInline, ]
    def get_form(self, request, obj=None, **kwargs):
        form = super(DGGSRegAdmin, self).get_form(request, obj, **kwargs)

        form.base_fields['basepoly'].queryset = Concept.objects.filter(scheme__uri=BASEPOLYHEDRON_CODELIST)
        form.base_fields['basepoly'].widget.can_add_related = False
        form.base_fields['refmodel'].queryset = Concept.objects.filter(scheme__uri=REFMODEL_CODELIST)
        form.base_fields['refmodel'].widget.can_add_related = False
        #=======================================================================
        # form.base_fields['celltype1'].queryset = Concept.objects.filter(scheme__uri=CELLTYPE_CODELIST)
        #=======================================================================
        #=======================================================================
        # form.base_fields['celltype'].queryset = Concept.objects.filter(scheme__uri=CELLTYPE_CODELIST)
        # form.base_fields['celledgetype'].queryset = Concept.objects.filter(scheme__uri=EDGETYPE_CODELIST)
        #=======================================================================
        form.base_fields['tessellation_method'].queryset = Concept.objects.filter(scheme__uri=TESSELLATION_CODELIST)
        form.base_fields['tessellation_method'].widget.can_add_related = False
        return form

class DGGSConformanceTestAdmin(admin.ModelAdmin):
    pass

class DGGSRequirementAdmin(admin.ModelAdmin):
    pass

class DGGSTessellationAdmin(admin.ModelAdmin):   
    def get_form(self, request, obj=None, **kwargs):
        form = super(DGGSTessellationAdmin, self).get_form(request, obj, **kwargs)
        
        form.base_fields['celltype'].queryset = Concept.objects.filter(scheme__uri=CELLTYPE_CODELIST)
        form.base_fields['celltype'].widget.can_add_related = False
        form.base_fields['celledgetype'].queryset = Concept.objects.filter(scheme__uri=EDGETYPE_CODELIST)
        form.base_fields['celledgetype'].widget.can_add_related = False
        return form    
        
admin.site.register(DGGSReg, DGGSRegAdmin)
admin.site.register(DGGSConformanceTest, DGGSConformanceTestAdmin)
admin.site.register(DGGSRequirement,DGGSRequirementAdmin)
admin.site.register(DGGSTessellation,DGGSTessellationAdmin)


