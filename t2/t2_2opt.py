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

from solver2opt import RouteFinder
dataset = input()
import math as m
import matplotlib.pyplot as plt
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
best_distance, best_route, visits = route_finder.solve()

print('distance', best_distance)
print('visits', visits)
print(best_route)

x = []
y = []

for i in range(0, len(best_route)):
  ind = int(best_route[i]) - 1
  x.append(float(cidades[ind][1]))
  y.append(float(cidades[ind][2]))

coord_x = []
coord_y = []

for i in cidades:
  coord_x.append(float(i[1]))
  coord_y.append(float(i[2]))

x.append(float(cidades[0][1]))
y.append(float(cidades[0][2]))

#plt.axis('off')
#plt.axis([20833.3333, 27462.5000, 10383.3333, 17100.0000])
plt.plot(coord_x, coord_y, 'o', x, y)
plt.savefig('grafico.png')
plt.show()
