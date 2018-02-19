# -*- coding: utf-8 -*-

from django.db import models

from skosxl.models import *

DEFS_BASE='https://www.opengis.net/def/dggs/code/'
BASEPOLYHEDRON_CODELIST="".join((DEFS_BASE,"basepoly"))
REFMODEL_CODELIST="".join((DEFS_BASE,"refmodel"))
CELLTYPE_CODELIST="".join((DEFS_BASE,"celltype"))

class DGGSReg(models.Model):
    uri = models.URLField(help_text=u'URI identifying the DGGS')
    name = models.CharField(max_length=100,help_text=u'Display name')
    basepoly = models.ForeignKey(Concept, related_name='basepoly',verbose_name="Base Polyhedron")
    refmodel = models.ForeignKey(Concept, related_name='refmodel',verbose_name="Earth Reference Model")
    celltype= models.ForeignKey(Concept, related_name='celltype',verbose_name="Cell Type")
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

