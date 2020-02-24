import pygame
import numpy as np
import tkinter as tk
from tkinter import *
from math import sqrt
from random import randint
import os
import sys
import itertools

class Serach:
	def __init__(self, dim):
		self._dim = dim
		self._nodes = []
		self._path_options = {}
		self._path = []
		self._opened_nodes = [start_node]
		self._current_node = None
		self._neighbors = {}
		self._wall_nodes = []
		self._h = {}
		self._g = {}
		self._f = {}


		# init functions
		self.allNodes()
		self.wallNodes()
		self.neigbourgs()
		self.FGH()

	def allNodes(self):
		for i in range(self._dim):
			for j in range(self._dim):
				self._nodes.append((i, j))


	def neigbourgs(self):
		posibilities = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
		for node in self._nodes:
			is_neighbor = []
			for i in posibilities:
				temp = node[0]+i[0], node[1]+i[1]
				if temp in self._nodes:
					is_neighbor.append(temp)
			self._neighbors[node] = is_neighbor


	def pathAppend(self, node):
		self._path.append(node)

	def examinedAppend(self, node):
		self._examined_nodes.append(node)

	def getNeighbors(self, node):
		return self._neighbors[node]

	def removeWallNodes(self):
		if self._wall_nodes == []:
			print("Nothing was deleted")
		elif type(self._wall_nodes) == type((0,0)) and len(self._wall_nodes) == 2:
			del self._nodes[node]
		elif type(self._wall_nodes) == type([]) and type(self._wall_nodes[0]) == type((0,0)) and len(self._wall_nodes[0]) == 2:
			for i in self._wall_nodes:
				if i in self._nodes:
					del self._nodes[self._nodes.index(i)]
		else:
			print("Nothing was deleted")

	def FGH(self):
		for node in self._nodes:
			self._h[node] = sqrt((node[0] - end_node[0])**2 + (node[1] - end_node[1])**2)
			self._g[node] = sys.float_info.max
			self._f[node] = sys.float_info.max
		self._g[start_node] = 0
		self._f[start_node] = self._h[start_node]

	def euclidian(self, node):
		return sqrt((node[0] - self._current_node[0])**2 + (node[1] - self._current_node[1])**2)

	def wallNodes(self):
		for node in range(int(dim_size*dim_size*.33)):
			i = randint(0,dim_size-1)
			j = randint(0,dim_size-1)
			if (i, j) in self._nodes and (i, j) != start_node and (i, j) != end_node:
				self._wall_nodes.append((i, j))
			self.removeWallNodes()

	def getWallNodes(self):
		return self._wall_nodes
	def getPath(self):
		self._path.reverse()
		return self._path


	def aStar(self):
		while len(self._opened_nodes) != 0:
			f_temp = {key : self._f[key] for key in self._opened_nodes}
			self._current_node = min(f_temp, key=f_temp.get)
			if self._current_node == end_node:
				print("Path found")
				self.obtainPath()
				return True
			self._opened_nodes.remove(self._current_node)
			for node in self._neighbors[self._current_node]:
				g_temp = self._g[self._current_node] + self.euclidian(node)
				if self._g[node] > g_temp:
					self._path_options[node] = self._current_node
					self._g[node] = g_temp
					self._f[node] = self._g[node] + self._h[node]
					if node not in self._opened_nodes:
						self._opened_nodes.append(node) 
				
		print("No path found")
		return False

	def obtainPath(self):
		node = end_node
		self._path.append(end_node)
		while node != start_node:
			self._path.append(self._path_options[node])
			node = self._path_options[node]



def drawGrid(surface):
	white = (225, 225, 225)
	grid_dim = pygame.display.get_surface().get_size()[0]//(square_dim + margin)
	for i in range(grid_dim):
		for j in range(grid_dim):
			pygame.draw.rect(surface, white, (j*(square_dim+margin)+margin, i*(square_dim+margin)+margin, square_dim, square_dim))

def drawWall(surface, nodes):
	black = (0, 0, 0)
	for node in nodes:
		# Draw rectangle walls
		# pygame.draw.rect(surface, black, (node[1]*(square_dim+margin)+margin, node[0]*(square_dim+margin)+margin, square_dim, square_dim))
		# Draw circle walls
		pygame.draw.circle(surface, black, (node[1]*(square_dim+margin)+margin+square_dim//2, node[0]*(square_dim+margin)+margin+square_dim//2), int(square_dim/2))

def drawPath(surface, path):
	blue = (0, 0, 255)
	for i in range(len(path)-1):
		pygame.draw.line(surface, blue, (path[i][1]*(square_dim+margin)+square_dim/2, path[i][0]*(square_dim+margin)+square_dim/2), (path[i+1][1]*(square_dim+margin)+square_dim/2, path[i+1][0]*(square_dim+margin)+square_dim/2), int(square_dim/2))





# Grid dimmensions
margin = 1
win_dim = 400
dim_size = 20
square_dim = int((win_dim - dim_size) / dim_size)
FPS = 60
start_node = (0, 0)
end_node = (dim_size - 1, dim_size - 1)


pygame.init()
window = pygame.display.set_mode((win_dim, win_dim))
pygame.display.set_caption('A*')
clock = pygame.time.Clock()

state = Serach(dim_size)
drawGrid(window)
wall_nodes = state.getWallNodes()
drawWall(window, wall_nodes)
state.aStar()
path = state.getPath()
drawPath(window, path)


done = False
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()
