#!/bin/python
# -*- coding: utf-8 -*-

__author__="Johann Lecocq(johann-lecocq.fr)"
__license__ = "GNU GENERAL PUBLIC LICENSE version 2"
__version__ = "1.0"

import unittest
from polygone import Polygone

#polygone A(5,2) B(5,7) C(11,8) D(11,11) E(8,11) F(8,9) G(6,9) H(6,14) I(11,14) Q(14,10) J(12,2)
#points K(7,10) / L(3,5) / M(3,17) / N(7,2) / R(6,12)

class TestPolygone(unittest.TestCase):
	'''Test sur le polygone ABCDEFGHIQJ'''
	def setUp(self):
		self.polygone=Polygone()
		sommets=[(5,2),(5,7),(11,8),(11,11),(8,11),(8,9),(6,9),(6,14),(11,14),(14,10),(12,2)]
		self.polygone.ajoute_liste_point(sommets)
		self.polygone.initialiser()
	def test_contient_sommet(self):
		self.assertTrue(self.polygone.contient(11,11))
	def test_contient_intersection_trois_segement_et_sommet(self):
		self.assertTrue(self.polygone.contient(7,10))
	def test_contient_segment_horizontal(self):
		self.assertTrue(self.polygone.contient(7,2))
	def test_contient_segment_vertical(self):
		self.assertTrue(self.polygone.contient(6,12))
	def test_dehors_intersection_directe_deux_segements(self):
		self.assertFalse(self.polygone.contient(3,5))
	def test_dehors_sans_intersection_directe(self):
		self.assertFalse(self.polygone.contient(3,17))
	

if __name__ == "__main__":
	unittest.main()
