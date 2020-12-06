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

from py2opt.routefinder import RouteFinder
import math as m
import matplotlib.pyplot as plt

dataset = input()
ref_arq = open(dataset)

cidades = []

for line in ref_arq:
  cidade = line.split()
  cidades.append(cidade)

custos = []

for i in range(0, len(cidades)):
  coord = (cidades[i][1], cidades[i][2])
  distancia = calcula_distancias(coord, cidades)
  custos.append(distancia)

name = []
for i in range(0, len(cidades)):
  name.append(str(cidades[i][0]))

route_finder = RouteFinder(custos, name, iterations=5)
best_distance, best_route = route_finder.solve()

print(best_distance)
print(best_route)

x = []
y = []

for i in range(0, len(best_route)):
  ind = int(best_route[i]) - 1
  x.append(cidades[ind][1])
  y.append(cidades[ind][2])

coord_x = []
coord_y = []

for i in cidades:
  coord_x.append(i[1])
  coord_y.append(i[2])

x.append(cidades[0][1])
y.append(cidades[0][2])

plt.axis('off')
plt.plot(coord_x, coord_y, 'o', x, y)
plt.savefig('grafico.png')
plt.show()