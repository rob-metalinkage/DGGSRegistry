from django.forms import modelformset_factory, ModelForm, Form
from django import forms
from .models import * 
from skosxl.models import *


class DGGSTessellationForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(DGGSTessellationForm, self).__init__(*args, **kwargs)  
        self.fields['celltype'].queryset = Concept.objects.filter(scheme__uri=CELLTYPE_CODELIST)
        self.fields['celledgetype'].queryset = Concept.objects.filter(scheme__uri=EDGETYPE_CODELIST)
    
    class Meta:
        model = DGGSTessellation
        exclude=()
       
  

TessellationModelFormset = modelformset_factory(DGGSTessellation,
                                                form=DGGSTessellationForm,
                                                exclude=(),
                                               
                                                extra=1)


#===============================================================================
# class DGGSConformanceTestForm(ModelForm):
#     
#     def __init__(self, *args, **kwargs):
#         super(DGGSConformanceTestForm, self).__init__(*args, **kwargs)  
#         self.fields['celltype'].queryset = Concept.objects.filter(scheme__uri=CELLTYPE_CODELIST)
#         self.fields['celledgetype'].queryset = Concept.objects.filter(scheme__uri=EDGETYPE_CODELIST)
#     
#     class Meta:
#         model = DGGSConformanceTest
#         exclude=()
#===============================================================================

ConformanceTestModelFormset = modelformset_factory(DGGSConformanceTest,
                                                #===============================
                                                # form=DGGSConformanceTestForm,
                                                #===============================
                                                exclude=(),
                                                extra=18,
                                                max_num=18)

#===============================================================================
# DGGSRegModelFormset = modelformset_factory(DGGSReg,
#                                             exclude=())
#===============================================================================

class DGGSRegForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(DGGSRegForm, self).__init__(*args, **kwargs)  
        self.fields['basepoly'].queryset = Concept.objects.filter(scheme__uri=BASEPOLYHEDRON_CODELIST)
        self.fields['refmodel'].queryset = Concept.objects.filter(scheme__uri=REFMODEL_CODELIST)
        self.fields['tessellation_method'].queryset = Concept.objects.filter(scheme__uri=TESSELLATION_CODELIST)
        
        self.fields['uri'].widget.attrs['style'] = 'width:400px'
        self.fields['name'].widget.attrs['style'] = 'width:400px'
        
    class Meta:
        model = DGGSReg
        fields = ['uri',  
                  'name',  
                  'basepoly',  
                  'basepoly_ref',  
                  'refmodel', 
                  'refinement_ratio', 
                  'tessellation_method']
        

class DGGSReg_selectionForm(Form):  
    _dggs_list = (("-","------"),)
    dggs_comboBox = forms.ChoiceField(choices=_dggs_list,
                                                      required=True,
                                                      initial='-')     
    def __init__(self, *args, **kwargs):
        super(DGGSReg_selectionForm, self).__init__(*args, **kwargs)  
        dggs_registry_details = DGGSReg.objects.all() 
        dggs_registry_details_list = list(dggs_registry_details.values_list("id","name"))
        dggs_registry_details_list.insert(0,('-','----------'))
      
        self.fields['dggs_comboBox'].label = "Select DGGS Spec to Review:"
        self.fields['dggs_comboBox'].choices = tuple(dggs_registry_details_list)
        