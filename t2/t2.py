from __future__ import print_function
from ortools.linear_solver import pywraplp
from graphviz import Digraph
import math as m

# Funcao para calcular a aresta de menor custo dado um indice "index"
def search_min_cost(index, arr, visited, dim):
	min = 10000000.0
	node = -1
	for i in range(0, dim):
		if(arr[index][i] < min and visited[i] != True):
			min = arr[index][i]
			node = i
	return node

def calcula_distancias(cidade, cidades):
	distancias = []
	for i in range(0, len(cidades)):
		a = float(cidades[i][1]) - float(cidade[0])
		b = float(cidades[i][2]) - float(cidade[1])
		dist = m.sqrt((m.pow(a, 2) + m.pow(b, 2)))
		#print(f'A distância entre os pontos {cidade[0]}, {cidade[1]} e {cidades[i][1]}, {cidades[i][2]} é: {dist}')
		if dist == 0:
			dist = 1000000.0
		distancias.append(dist)
	return distancias

solver = pywraplp.Solver.CreateSolver('SCIP')
#solver = pywraplp.Solver('simple_lp_program',
#                          pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
solver.set_time_limit(600000) # Configura o tempo limite para 10 segundos

ref_arq = open('../data_points/uruguay.tsp') # Le o arquivo no qual contem as coordenadas das cidades

cidades = []

for line in ref_arq:
	cidade = line.split()
	cidades.append(cidade)

custos = []

for i in range(0, len(cidades)):
	coord = (cidades[i][1], cidades[i][2])
	distancia = calcula_distancias(coord, cidades)
	custos.append(distancia)

# As variaveis abaixo servem para calcular, utilizando abordagem "gulosa", o caminho de menor custo 
visitado = [False for i in range(0, len(cidades))]
seq_vis = [-1 for i in range(0, len(cidades))]
index = 0
visitado[index] = True
edge = 0
for i in range(0, len(cidades)):
	edge = search_min_cost(index, custos, visitado, len(cidades))
	visitado[edge] = True
	seq_vis[index] = edge
	index = edge

# print(seq_vis)
# for i in range(0, len(cidades)):
#   for j in range(0, len(cidades)):
#     print(str(i)+ ' -> ' +str(j)+ ' = ' +str(custos[i][j]))
#   print("\n")

num_cidades = len(custos)

#dot = Digraph(comment='TSP Galaxies') # Cria o grafo direcionado
#dot.format = 'jpg' # Muda o formato do arquivo de saida

#for i in range(num_cidades): # Adiciona os nohs ao grafo
#    dot.node(str(i), str(i))


# --------------- Definicoes das variaveis ------------------
# x[i, j] corresponde aos xij do problema, e sao 0 ou 1
x = {}
for i in range(num_cidades):
    for j in range(num_cidades):
        x[i, j] = solver.IntVar(0.0, 1.0, '')



# mp_variables = []
# mp_values = []
# Forca 92% dos nohs para serem 1 (isso diminui muito o tempo que leva para calcular a rota otima)
for i in range(0, round(len(seq_vis) * 0.92)):
	if(seq_vis[i] != -1):
		x[i, seq_vis[i]] = solver.IntVar(1.0, 1.0, '')
		# mp_variables.append(x[i, seq_vis[i]])
		# mp_values.append(1.0)
		


# **********  TESTANDO SetHint e valores forcados *********** #
# mp_variables = [x[0, 1], x[1, 5], x[5, 9], x[9, 10], x[10, 11], x[11, 12], x[12, 13], x[13, 16], x[16, 17], x[17, 18], x[18, 21], x[21, 22], x[22, 28], x[28, 27]]
# mp_values = [1.0 , 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
# solver.SetHint(mp_variables, mp_values)
# x[0, 1] = solver.IntVar(1, 1, '')
# x[1, 5] = solver.IntVar(1, 1, '')
# x[5, 9] = solver.IntVar(1, 1, '')
# x[9, 10] = solver.IntVar(1, 1, '')
# x[10, 11] = solver.IntVar(1, 1, '')
# x[11, 12] = solver.IntVar(1, 1, '')
# x[12, 13] = solver.IntVar(1, 1, '')
# x[13, 16] = solver.IntVar(1, 1, '')
# x[16, 17] = solver.IntVar(1, 1, '')
# x[17, 18] = solver.IntVar(1, 1, '')
# x[18, 21] = solver.IntVar(1, 1, '')
# x[21, 22] = solver.IntVar(1, 1, '')
# x[22, 28] = solver.IntVar(1, 1, '')
# x[28, 27] = solver.IntVar(1, 1, '')
# *********************  FIM TESTANDO ********************* #

y = {}
for i in range(num_cidades):
	y[i] = solver.IntVar(1, (num_cidades - 1), '')
# --------------- End Definicoes das variaveis --------------



# ------------------------  Restricoes ----------------------
# Garante que cada vertice so pode ser visitado uma unica vez
for i in range(num_cidades):
    solver.Add(solver.Sum([x[i, j] for j in range(num_cidades)]) == 1)

# Garante que, ao sair de uma galaxia, tenha-se somente uma outra galaxia como destino
for j in range(num_cidades):
    solver.Add(solver.Sum([x[i, j] for i in range(num_cidades)]) == 1)

# Garante que nao havera subrotas
for i in range(1, num_cidades):
   for j in range(1,  num_cidades):
      solver.Add((x[i, j] * (num_cidades - 1) + y[i] - y[j]) <= (num_cidades - 2))
# --------------------- End Restricoes ---------------------



# --------------------  Funcao Objetivo --------------------
objective_terms = []
for i in range(num_cidades):
    for j in range(num_cidades):
        objective_terms.append(custos[i][j] * x[i, j])
solver.Minimize(solver.Sum(objective_terms))
# ------------------  End Funcao Objetivo ------------------

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
	print('Total cost = ', round(solver.Objective().Value(), 1), '\n')
	count = 0
	i = 0
	while (count < len(custos)):
		for j in range(num_cidades):
			# Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
			if x[i, j].solution_value() == 1.0:
				print('%d -> %d.  Cost = %d' %
					(i, j, custos[i][j]))
				#dot.edge(str(i), str(j), constraint='false', label=str(custos[i][j])) # Adiciona as arestas no grafo
				i = j
				break
		count += 1

#dot.render('grafo') # Salva o arquivo no formato SVG
