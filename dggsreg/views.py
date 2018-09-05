# -*- coding: utf-8 -*-
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from django.http import HttpResponse
from django.shortcuts import render, redirect
import json
from pprint import pprint

from .models import (
    #===========================================================================
    # Era,
    # EraScheme,
    #===========================================================================
    DGGSReg,
    DGGSTessellation
)

from .forms import * #TessellationModelFormset, DGGSRegForm


#===============================================================================
# class eraCreateView(CreateView):
# 
#     model = Era
# 
# 
# class eraDeleteView(DeleteView):
# 
#     model = Era
# 
# 
# class eraDetailView(DetailView):
# 
#     model = Era
# 
# 
# class eraUpdateView(UpdateView):
# 
#     model = Era
# 
# 
# class eraListView(ListView):
# 
#     model = Era
# 
# def eraIntervals(request,scheme_id):
#     if request.GET.get('pdb') :
#         import pdb; pdb.set_trace()
#     try:
#         start = int(request.GET.get('start'))
#     except:
#         start = None
#     try:
#         end = int(request.GET.get('end'))
#     except:
#         end = None        
#     scheme = EraScheme.objects.get(id=scheme_id)
#     return HttpResponse(    scheme.json_intervals(start=start,end=end),  content_type="application/json")
#    
# 
# def eraTimeline(request,scheme_id):
#     """Generate a d3 interactive timeline vizualisation
#     
#     Hierarchical D3 viz, with zoom and link to details. Todo. Todo later still... make link configurable
#     """
#     model = EraScheme
#===============================================================================


def dggs_registry(request):
    dggs_registry_details = DGGSReg.objects.all() 
    
    dggs_registry_list = []
    for rec in dggs_registry_details:
        dggs_entry = {'name': rec.name,
                      'basepoly': rec.basepoly,
                      'basepoly_ref': rec.basepoly_ref,
                      
                      'cellequalarea': rec.cellequalarea,
                      
                      'refmodel': rec.refmodel,
                      
                      'refinement_ratio': rec.refinement_ratio,
                      'uri': rec.uri,
                      'dggstessellation_set': [{'refinement_level': d.refinement_level,
                                                   'celltype': d.celltype,
                                                   'celledgetype': d.celledgetype,
                                                   'number_of_cells': d.number_of_cells,
                                                   'cellarea': d.cellarea,
                                                   'cellarea_precision': d.cellarea_precision} for d in rec.dggstessellation_set.all()],
                      'dggsconformancetest_set': [{'requirement': d.requirement.name,
                                                   'status': d.status,
                                                   'notes': d.notes} for d in rec.dggsconformancetest_set.all()],

                      }
        pprint(dggs_entry)
        dggs_registry_list.append(dggs_entry)
    
    requirements_list = DGGSRequirement.objects.all()
    requirements_list = [req[0] for req in list(requirements_list.values_list("name"))]
    
    context = {'dggs_registry_list': dggs_registry_list,
               'requirements_list': requirements_list}
    return render(request, 'current_registry.html', context)



def select_dggs_spec(request):
    if request.method == 'GET':
        dggs_selection_form = DGGSReg_selectionForm()
        context = {'dggs_selection_form': dggs_selection_form}
        return render(request, 'select_dggs_for_review.html', context)

    elif request.method == 'POST':
        dggs_spec = DGGSReg.objects.filter(id = request.POST['dggs_comboBox'])
        
        return redirect('review_dggs_spec', id=dggs_spec[0].id) 
    
    
def review_dggs_spec(request, id=0):
    if request.method == 'GET':
        dggs_spec = DGGSReg.objects.filter(id = id)
        
        dggs_entry = {'name': dggs_spec[0].name,
                      'basepoly': dggs_spec[0].basepoly,
                      'basepoly_ref': dggs_spec[0].basepoly_ref,
                      
                      'cellequalarea': dggs_spec[0].cellequalarea,
                      
                      'refmodel': dggs_spec[0].refmodel,
                      
                      'refinement_ratio': dggs_spec[0].refinement_ratio,
                      'uri': dggs_spec[0].uri,
                      'dggstessellation_set': [{'refinement_level': d.refinement_level,
                                                   'celltype': d.celltype,
                                                   'celledgetype': d.celledgetype,
                                                   'number_of_cells': d.number_of_cells,
                                                   'cellarea': d.cellarea,
                                                   'cellarea_precision': d.cellarea_precision} for d in dggs_spec[0].dggstessellation_set.all()],
                      'dggsconformancetest_set': [{'requirement': d.requirement.name,
                                                   'status': d.status,
                                                   'notes': d.notes} for d in dggs_spec[0].dggsconformancetest_set.all()],

                      }
        initial_requirements_list = DGGSRequirement.objects.all()        
        initial_requirements_list = list(initial_requirements_list.values_list("id"))
        initial_conformance_test_list = []
        for reqid in initial_requirements_list:
            initial_conformance_test_list.append({
                                                  'requirement': reqid[0]})
        
        if len(dggs_entry['dggsconformancetest_set']) == 0:
            formset = ConformanceTestModelFormset(queryset=DGGSConformanceTest.objects.none(),
                                                  
                                                    initial = initial_conformance_test_list,)
        else:
            formset = ConformanceTestModelFormset(queryset=dggs_spec[0].dggsconformancetest_set.all(),
                                                  )
        
        context = {'dggs_spec': dggs_entry,
                   'formset': formset}
        return render(request, 'review_dggs.html', context)


        
    elif request.method == 'POST':
        post_values = request.POST.copy()
        for i in range(int(post_values['form-TOTAL_FORMS'])):
            post_values['form-'+str(i)+'-dggs'] = id
            post_values['form-'+str(i)+'-id'] = list(DGGSConformanceTest.objects.filter(dggs = id,
                                                    requirement = i+1).values_list("id"))[0][0]                    
           
        formset = ConformanceTestModelFormset(post_values)
        if formset.is_valid():
            for form in formset:
                
                form.save()
            
            return redirect('review_dggs_spec_complete')
    
def review_dggs_spec_complete(request): 
    return render(request, 'review_dggs_complete.html')
    

def submit_new_dggs(request):
    if request.method == 'GET':
        dggs_specs_form = DGGSRegForm(DGGSReg.objects.none())
        formset = TessellationModelFormset(queryset=DGGSTessellation.objects.none())
        
    elif request.method == 'POST':
        post_values = request.POST.copy()
        dggs_specs_form = DGGSRegForm(post_values)
        if dggs_specs_form.is_valid():
            dggs_specs_form.save()
           
        #=======================================================================
        # link the tessellation forms to the master DGGS Registration Form
        #=======================================================================
        for i in range(int(post_values['form-TOTAL_FORMS'])):
            post_values['form-'+str(i)+'-dggs'] = DGGSReg.objects.get(name=request.POST['name']).id
        formset = TessellationModelFormset(post_values)
       
        if formset.is_valid():
            for form in formset:
                form.save()
            
            return redirect('submit_new_dggs_success')
    
    context = {'dggs_specs_form': dggs_specs_form,
                'formset': formset}
    return render(request, 'submit_new_dggs.html', context)
    
def submit_new_dggs_success(request): 
    return render(request, 'submit_new_dggs_success.html')