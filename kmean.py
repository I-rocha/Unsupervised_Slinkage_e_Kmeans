import re
import math
import matplotlib.pyplot as plt
import random

'''
Recebe dois pares ordenados e retorna a distancia
# p1: Par ordenado 1
# p2: Par ordenado 2
'''
def euclidian_distance(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return math.sqrt(dx**2 + dy**2)

'''
Compara se dois vetores 1D são iguais
# vec1: Vetor 1
# vec2: Vetor 2
# return: True se igual ou False se diferente

'''
def equal_vec(vec1, vec2):
    if len(vec1) != len(vec2):
        return False
    
    for v1, v2 in zip(vec1, vec2):
        if v1 != v2:
            return False
    return True
'''
Abre arquivo e faz a leitura dos dados. Dados precisam ter 2 colunas de atributo e 1 de classificação
# path: caminho completo do arquivo
'''
def begin(path):
    fd = open(path)
    dt = []
    for line in fd:
        a1, a2, c1, sp = re.split('\n|\t', line)
        dt.append([float(a1), float(a2), int(c1)])
    fd.close()
    return dt

class Data:
    def __init__(self, attr, cls):
        self.attr = attr
        self.cls = cls

    def print_d(self):
        for i in self.attr:
            print('A1: {0} A2: {1}'.format(i[0], i[1]))

    def print_cls(self):
        for i in self.cls:
            print(i)

class KMean:
    '''
    # k: Quantidade de classes iniciais
    # vlim: Valores de limite
    # data: Dados de atributo
    ''' 
    def __init__(self, k, data):    
        self.k = k
        self.state = []
        self.x = [x[0] for x in data.attr]
        self.y = [y[1] for y in data.attr]
        self.xminmax = [min(self.x), max(self.x)]
        self.yminmax = [min(self.y), max(self.y)]
        self.vlim = self.random_limits()

        if len(self.vlim) != self.k:
            print('ERR: Quantidade de classes e valores de limites diferentes')
        

    '''
    Calcula o proximo estado baseado nos valores de limites
    # return: lista com valores de classes preditas do estado atual
    '''
    def __next_state(self):    
        dist_lim = []
        pred = []
        for x,y in zip(self.x, self.y):
            dist = []
            for i in range(self.k):
                eucl = euclidian_distance([x, y], self.vlim[i])
                dist.append(eucl)
        
            dist_lim.append(dist)
    
        for el in dist_lim:
            idx_min = min(range(self.k), key = lambda x: el[x])
            pred.append(int(idx_min))    # Classe prevista
        return pred

    '''
    Atualiza o valor de cada limite
    # state: estado atual (classificação atual de cada elemento)
    '''
    def __update_lim(self, state):
        centroid = []
        sum_cxy = [[0,0]]*self.k
        sz_c = [0]*self.k
        xmin, xmax = self.xminmax[0], self.xminmax[1]
        ymin, ymax = self.yminmax[0], self.yminmax[1]

        for x, y, cls in zip(self.x, self.y, state):
            # update x += xold
            xsum = sum_cxy[cls][0] + x

            # update y += yold
            ysum = sum_cxy[cls][1] + y  

            sum_cxy[cls] = [xsum, ysum]
            sz_c[cls] += 1
        
        for sum_xy, sz in zip(sum_cxy, sz_c):
            # Se uma classe não tiver elementos
            if sz == 0:
                # Gera uma posição aleatório de centro da classe
                xnew = round(random.uniform(xmin, xmax), 2)
                ynew = round(random.uniform(ymin, ymax), 2)
            else:
                xnew = (sum_xy[0]/sz)
                ynew = (sum_xy[1]/sz)
                
            centroid.append([xnew, ynew])

        self.vlim = centroid
        return

    '''
    Imprime os valores usados de limites
    '''
    def print_lim(self):
        print('Limites: ', self.vlim)

    '''
    Faz a classificação
    # epoch: Quantidade de iterações máxima que será realizada
    # return <predict>: Lista com a classificação de cada elemento
    # return <it>: Quantidade de iterações até o resultado final
    '''
    def classify(self, epoch):
        last_predict = []
        predict = []
        it = int(0)

        # Primeiras ocorrencias
        # previsão
        predict = self.__next_state()

        # Condição de parada
        while (not equal_vec(predict, last_predict)) & (it < epoch):
            
            # Descomente esse trecho caso queira ver o plot do grafico a cada iteração
            '''
            # Grafico
            plt.grid()
            plt.title(("Iteração:" + str(it) + "/" + str(epoch)))
            #plt.xticks([(x/2) for x in range(30)])
            #plt.yticks([(y/2) for y in range(30)])
            plot_data(plt, [[x,y] for x,y in zip(self.x, self.y)], predict)
            plot_lim(plt, self.vlim)
            plt.draw()
            plt.pause(0.25)
            plt.clf()
            '''

            # Atualiza epoca
            it += 1

            # Atualiza limites de acordo com a previsão
            self.__update_lim(predict)

            # Armazena estado da previsão passada
            last_predict = predict

            # Armazena estado da previsão atual
            predict = self.__next_state()

        return predict, it
    
    '''
    Calcula aleatoriamente os limites
    return: Centroides
    '''
    def random_limits(self):
        centroids = []
        digits = 2
        for i in range(self.k):
            xmin, xmax = self.xminmax
            ymin, ymax = self.yminmax
            randx = round(random.uniform(xmin, xmax), digits)
            randy = round(random.uniform(ymin, ymax), digits)
            
            centroids.append([randx, randy])
        return centroids

def plot_data(plt, pt, cls):
    color = ['red', 'green', 'lightblue', 'pink', 'purple']
    
    for p, c in zip(pt, cls):
        plt.plot(p[0], p[1], marker = 'o', markersize=10, markeredgecolor = 'black', markerfacecolor=color[c])

def plot_lim(plt, lim):
    color = ['red', 'green', 'lightblue', 'pink', 'purple']
    count = int(0)
    for l in lim:
        plt.plot(l[0], l[1], marker='*', markersize=15, markerfacecolor=color[count], markeredgecolor='black', markeredgewidth=3)
        count += 1



if __name__ == '__main__':
    #fname = 'teste.txt'
    fname = 'Aggregation.txt'
    pre_dt = begin(fname)
    dt = Data([[x[0], x[1]] for x in pre_dt], [x[2] for x in pre_dt])

    # Parametros
    groups = 3
    max_it = 20

    # Algoritmo
    kmean = KMean(groups, dt)
    predict, it = kmean.classify(max_it)

    # Grafico
    
    # Descomente esse trecho caso queira ver o plot do resultado final
    plt.grid()
    plt.title(("Iteração final: " + str(it) + "/" + str(max_it) + "\nQuantidade de grupos:") + str(groups))
    #plt.xticks([(x/2) for x in range(30)])
    #plt.yticks([(y/2) for y in range(30)])
    plot_data(plt, dt.attr, predict)
    plot_lim(plt, kmean.vlim)
    plt.show()
    
    print('In ', it, 'iterations, classification:\n', predict)
