#!/bin/python
# -*- coding: utf-8 -*-

__author__="Johann Lecocq(johann-lecocq.fr)"
__license__ = "GNU GENERAL PUBLIC LICENSE version 2"
__version__ = "1.0"

from itertools import chain, islice
from fractions import Fraction

def morceaux(iterable):
	"""parcours un iterable deux par deux
		iterable->(int,int)
	"""
	it = iter(iterable)
	premier=it.__next__()
	while True:
		last=it.__next__()
		yield (premier,last)
		premier=last

def cote_polygone(liste_cote):
	"""prends une liste de sommet de polygone
		et renvoie tous les cotés de celui-ci
		list((int,int))->list(((int,int),(int,int)))
		"""
	droites=[]
	for i in morceaux(liste_cote):
		droites.append(i)
	droites.append((liste_cote[-1],liste_cote[0]))
	return droites
	
def min_max_point(x,y):
	"""renvoie un tuple avec le min et le max trié
		int,int->(int,int)
	"""
	if x<y:
		return (x,y)
	return (y,x)

def intersection_verticale(point1,point2,x,y):
	"""resouds l'equation verticale et regarde si le point est situé a la droite de la droite
		retourne les coordonnés de l'intersection
		(int,int),(int,int),int,int->(int,int)
	"""
	yMin,yMax=min_max_point(point1[-1],point2[-1])
	if point1[0]>x and yMin<=y and y<=yMax:
		return (point1[0],y)
	else:
		return None
	
def intersection(equation,point1,point2,x,y):
	"""resouds l'equation et regarde si le point appartient au segement
		retourne les coordonnés de l'intersection
		(int,int),(int,int),int,int->(int,int)
	"""
	xRes=(y-equation.arg["b"])/equation.arg["a"]
	(x1,x2)=min_max_point(point1[0],point2[0])
	(y1,y2)=min_max_point(point1[-1],point2[-1])
	if y1<=y and y<=y2 and x1<=xRes and xRes<=x2 and x<=xRes:
		return (xRes,y)
	else:
		return None

class Equation:
	"""represente une equation du premier degré"""
	TYPE_VERTICALE=0
	TYPE_HORIZONTALE=1
	TYPE_NORMALE=2
	def __init__(self):
		self.type=2
		self.arg={"y":0,"x":0,"a":0,"b":0}
	def initialiser(self,cood1,cood2):
		"""initialise l'equation avec les coordonées passé en parametre"""
		if cood1[0]==cood2[0]:
			self.type=Equation.TYPE_VERTICALE
			self.arg["x"]=Fraction(cood1[0])
		elif cood1[1]==cood2[1]:
			self.type=Equation.TYPE_HORIZONTALE
			self.arg["y"]=Fraction(cood1[1])
		else:
			self.type=Equation.TYPE_NORMALE
			self.arg["a"]=Fraction(cood1[1]-cood2[1],cood1[0]-cood2[0])
			self.arg["b"]=Fraction(cood1[1]-self.arg["a"]*cood1[0])
	def is_verticale(self):
		"""retourne True si l'equation est verticale"""
		return self.type==Equation.TYPE_VERTICALE
	def is_horizontale(self):
		"""retourne True si l'equation est horizontale"""
		return self.type==Equation.TYPE_HORIZONTALE
	def __str__(self):
		if self.type==Equation.TYPE_VERTICALE:
			return "V  x="+str(self.arg["x"])
		elif self.type==Equation.TYPE_HORIZONTALE:
			return "H  y="+str(self.arg["y"])
		return "Y  y="+str(self.arg["a"])+"x +"+str(self.arg["b"])

class Polygone():
	"""represente un polygone"""
	def __init__(self):
		"""initialisation du polygone"""
		self.point = {}
		self.equation = {}
		self.nombre = 1
	def ajoute_point(self, x, y):
		"""ajoute un point au polygone"""
		self.point[self.nombre] = (x, y)
		self.nombre += 1
	def ajoute_liste_point(self,pol):
		"""ajoute une liste de point sous forme de tuple"""
		for x,y in pol:
			self.ajoute_point(x,y)
	def generer_equation(self):
		"""generation des equation en fonction des sommets du polygone"""
		l=list(self.point.keys())
		l.sort()
		for point1,point2 in cote_polygone(l):
			cood1=self.point[point1]
			cood2=self.point[point2]
			equation=Equation()
			equation.initialiser(cood1,cood2)
			self.equation[(point1,point2)]=equation
	def initialiser(self):
		"""initialise le polygone"""
		self.generer_equation()
	def contient(self, x, y):
		"""regarde si le point appartient au polygone
			int,int->bool
		"""
		liste_intersection=[]
		if (x,y) in self.point.values():
			return True
		for droite,equation in self.equation.items():
			if equation.is_verticale():
				inter=intersection_verticale(self.point[droite[0]],self.point[droite[1]],x,y)
				if inter!=None and not inter in liste_intersection:
					liste_intersection.append(inter)
				continue
			elif equation.is_horizontale():
				point1,point2=self.point[droite[0]],self.point[droite[1]]
				xMin,xMax=min_max_point(point1[0],point2[0])
				if point1[-1]==y and xMin<x and x<xMax:
					return True
				continue
			inter=intersection(equation,self.point[droite[0]],self.point[droite[1]],x,y)
			if inter!=None and not inter in liste_intersection:
				liste_intersection.append(inter)
		return len(liste_intersection)%2==1
