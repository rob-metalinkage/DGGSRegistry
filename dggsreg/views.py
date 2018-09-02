# -*- coding: utf-8 -*-
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from django.http import HttpResponse
from django.shortcuts import render
import json
from pprint import pprint

from .models import (
    #===========================================================================
    # Era,
    # EraScheme,
    #===========================================================================
    DGGSReg
)


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
    dggs_registry_details = DGGSReg.objects.all() #.filter(show_record=True).exclude(date_published__gt=timezone.now()) 
    print(dggs_registry_details)
    print(dir(dggs_registry_details[0]))
    
    dggs_registry_list = []
    for rec in dggs_registry_details:
        print('---')
        print(dir(rec.dggsconformancetest_set))
        print(rec.dggsconformancetest_set.all()[0])
        print(rec.dggstessellation_set.all()[0])
        print(rec.dggstessellation_set.all()[0].refinement_level)
        print(rec.dggstessellation_set.all()[0].celltype)
        print(rec.dggstessellation_set.all()[0].celledgetype)
        print(rec.dggstessellation_set.all()[0].number_of_cells)
        print(rec.dggstessellation_set.all()[0].cellarea)
        print(rec.dggstessellation_set.all()[0].cellarea_precision)
        print(rec.dggsconformancetest_set.all()[0].status)
        print(rec.dggsconformancetest_set.all()[0].notes)
        
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
        #=======================================================================
        # rec.dggsconformancetest_set.values_list('requirement__id', flat=True),
        #=======================================================================
                      #=========================================================
                      # 'objects': rec.objects.values_list()
                      #=========================================================
                      }
        pprint(dggs_entry)
        dggs_registry_list.append(dggs_entry)
        #=======================================================================
        # print(asdf)
        #=======================================================================
    context = {'dggs_registry_list': dggs_registry_list}
    print('context:\n'+str(context))
    return render(request, 'current_registry.html', context)