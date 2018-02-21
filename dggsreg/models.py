# -*- coding: utf-8 -*-

from django.db import models

from skosxl.models import *

DEFS_BASE='https://www.opengis.net/def/dggs/code/'
BASEPOLYHEDRON_CODELIST="".join((DEFS_BASE,"basepoly"))
REFMODEL_CODELIST="".join((DEFS_BASE,"refmodel"))
CELLTYPE_CODELIST="".join((DEFS_BASE,"celltype"))
TESSELLATION_CODELIST="".join((DEFS_BASE,"tessellationmethod"))

class DGGSReg(models.Model):
    uri = models.URLField(help_text=u'URI identifying the DGGS')
    name = models.CharField(max_length=100,help_text=u'Display name')
    basepoly = models.ForeignKey(Concept, related_name='basepoly',verbose_name="Base Polyhedron Type")
    basepoly_ref = models.CharField(max_length=1000, verbose_name="Base Polyhedron Reference Point", help_text='Reference point location of primary face of base polyhedron (as 3D point in WKT syntax)')
    refmodel = models.ForeignKey(Concept, related_name='refmodel',verbose_name="Earth Reference Model",help_text='Reference Model for the Earth (or other planetary body)')
    refines = models.ForeignKey('DGGSReg', related_name='refines_grid', verbose_name="")
    refinement_level = 0
    refinement_ratio = models.PositiveSmallIntegerField(default=9, help_text='refinement ratio of DGGS tesselations (e.g. 1:4, 1:9 etc...)')
    tessellation_method = models.ForeignKey(Concept, related_name='polyhedralTessellation',verbose_name="Tessellation Method",help_text='Tessellation method used')
    
    celltype= models.ForeignKey(Concept, related_name='celltype',verbose_name="Cell Type")
    cellarea = models.FloatField(help_text='cell area for each level of refinement')
    cellarea_precision = models.FloatField(help_text='cell area precision for each level of refinement')
    
    cellequalarea = models.BooleanField(default=True, verbose_name="Cells have equal area", help_text="""
        If the DGGS implementation is more complex and has multiple classes of cell type where each cell in each class is equal area, 
        but each class has a different cell area (e.g. a Hexagonal refinement of an icosahedron will,
        in most cases, yield both hexagons and 12 pentagons centred on the vertices of the icosahedron 
        here each pentagon is 5/6 of the area of each hexagon) this is more challenging to show. 
        We either show a Yes/No flag as to whether or not the DGGS implementation has passed or failed the “Cell-area conformance test”
        (which can accommodate this complication); or, we show a more detailed breakdown of each cell type class 
        and how they relate to each other in terms of fixed areal difference.""" )
    
        
    def __unicode__(self):
        return ( self.name )
    
    def clean(self):
        
        """
    
        check that parent dggs tesselation/grid is not it's own parent
        - calculate refinement level of the tessellation
        """
        pass

class DGGSConformanceTests(models.Model):
    req_1_core_data_model = models.CharField(max_length=100,help_text='req_1_core_data_model')
    req_2_referenceframe_refmodelequalarea = models.CharField(max_length=100,help_text='req_2_referenceframe_refmodelequalarea')
    req_3_referenceframe_overlap = models.CharField(max_length=100,help_text='req_3_referenceframe_overlap')
    req_4_referenceframe_tessellation_sequence = models.CharField(max_length=100,help_text='req_4_referenceframe_tessellation_sequence')
    req_5_referenceframe_globalareapreservation = models.CharField(max_length=100,help_text='req_5_referenceframe_globalareapreservation')
    req_6_referenceframe_cellshape = models.CharField(max_length=100,help_text='req_6_referenceframe_cellshape')
    req_7_referenceframe_cellareaprecision = models.CharField(max_length=100,help_text='req_7_referenceframe_cellareaprecision')
    req_8_referenceframe_cellarea = models.CharField(max_length=100,help_text='req_8_referenceframe_cellarea')
    req_9_referenceframe_initialtessellation = models.CharField(max_length=100,help_text='req_9_referenceframe_initialtessellation')
    req_10_referenceframe_cellrefinement = models.CharField(max_length=100,help_text='req_10_referenceframe_cellrefinement')
    req_11_referenceframe_celladdressingmethod = models.CharField(max_length=100,help_text='req_11_referenceframe_celladdressingmethod')
    req_12_referenceframe_celladdressinguniqueindex = models.CharField(max_length=100,help_text='req_12_referenceframe_celladdressinguniqueindex')
    req_13_referenceframe_celladdressingcentroid = models.CharField(max_length=100,help_text='req_13_referenceframe_celladdressingcentroid')
    req_14_functionalalgorithms_quantizationoperations = models.CharField(max_length=100,help_text='req_14_functionalalgorithms_quantizationoperations')
    req_15_functionalalgorithms_cellnavigation = models.CharField(max_length=100,help_text='req_15_functionalalgorithms_cellnavigation')
    req_16_functionalalgorithms_spatialanalysis = models.CharField(max_length=100,help_text='req_16_functionalalgorithms_spatialanalysis')
    req_17_functionalalgorithms_queryoperations = models.CharField(max_length=100,help_text='req_17_functionalalgorithms_queryoperations')
    req_18_functionalalgorithms_broadcastoperations = models.CharField(max_length=100,help_text='req_18_functionalalgorithms_broadcastoperations')
    
    
    def __str__(self):
        return (self.name)