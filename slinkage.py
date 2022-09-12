import re
import math
import matplotlib.pyplot as plt
import time

'''
Distância euclidiana
p1: ponto (x1, y1)
p2: ponto (x2, y2)
return distancia
'''
def euclidian_distance(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return math.sqrt(dx**2 + dy**2)

'''
Dado uma matriz, e uma lista de minimos, encontra o elemento minimo
'''
def minimun(mat, lowests) -> 'Linha, coluna, valor':
    row = int(0)
    col = int(0)
    min_x = 0
    min_y = 0
    low = lowests[-1]

    for el in lowests:
        if row == 0:
            row+=1
            continue
        elif el <= low:
            min_x = row
            low = el
        row += 1

    line = mat[min_x]
    
    for el in line:
        if el == low:
            min_y = col
        col += 1
     
    return min_x, min_y, low

'''
Abre arquivo e retorna dados
'''
def begin(fpath):
    fd = open(fpath)
    dt = []
    for line in fd:
        attr1, attr2, cls, spc = re.split('\n|\t', line)
        dt.append([float(attr1), float(attr2), int(cls)])

    fd.close()
    return dt

class Linkage:
    def __init__(self, attr: 'atributos', cls: 'classes'):
        if len(attr) != len(cls):
            print('ERROR: atributos e classes de tamanho diferente')

        self.attr = attr
        self.cls = cls
        self.sz = len(cls)

    # Auto explicativo
    def print_cls(self):
        for el in self.cls:
            print(el)
            
    # Auto explicativo        
    def print_attr(self):
        for el in self.attr:
            print(str(el[0]) + ", " + str(el[1]))

    '''
    Calcula o custo da relação entre cada elemento
    return: Matriz triangular inferior inicial relacionando o custo de elementos 2 a 2
    '''
    def first_cost(self) -> list: 
        sz = self.sz
        cost =[]
        line = []
        
        for i in range (sz):
            line = []
            for j in range(0,i+1):
                p1 = self.attr[i]   # Elemento 1
                p2 = self.attr[j]   # Elemento 2
                line.append(euclidian_distance(p1, p2))
                
            cost.append(line)
        return cost
        
    '''
    Faz o agrupamento dos elementos em ordem de semelhança
    cset: Lista contendo cada conjunto/grupo atual
    epoch: Quantidade maxima de iterações
    epoch: Quantidade de grupos desejado
    return: 
    '''
    def group_all(self, cset: list, epoch = 1000, groups = 1) -> 'new list conjunto e novos custos':
        cost = self.first_cost()
        lowests = self.init_lowests(cost)
        new_set = []
        new_cost = []
        it = int(0)
        dtime_minimun = 0
        dtime_next_group = 0
        dtime_new_cost = 0
        
        if (not cost) | (not cset):
            return [], []
        
        while (it < epoch) & (len(cset) > groups):
            time_b = time.process_time()
            # Elemento de menor valor
            tidx_1, tidx_2, min_val = minimun(cost, lowests)
            
            time_a = time.process_time()
            
            dtime_minimun += time_a - time_b

            time_b = time.process_time()
            # Conjunto
            new_set = self.next_group(tidx_1, tidx_2, cset)
            cset = new_set
            time_a = time.process_time()

            dtime_next_group += time_a - time_b

            time_b = time.process_time()
            # Custo
            new_cost = self.next_cost(cost, tidx_1, tidx_2, lowests)
            cost = new_cost
            time_a = time.process_time()

            dtime_new_cost += time_a - time_b

            # Se lista vazia
            if not cost:
                return new_set, []

            it += 1
        print("Tempo minimun:", dtime_minimun)
        print("Tempo next_group:", dtime_next_group)
        print("Tempo new_cost:", dtime_new_cost)
        
        return new_set, new_cost
       
    '''
    Calcula o proximo agrupamento dado os dois elementos mais semelhante
    tidx_1: Indice do atributo alvo 1 mais semelhante
    tidx_2: Indice do atributo alvo 2 mais semelhante
    cset:   Conjunto de classes atual
    return: Novo conjunto classificado
    '''
    def next_group(self, tidx_1, tidx_2, cset):
        new_el =[]
        new_set =[]
        
        new_el = cset[tidx_1] + cset[tidx_2]
        
        for i in range (len(cset)):
            if i == tidx_2:
                new_set.append(new_el)
                
            elif i == tidx_1:
                continue
            
            else:
                new_set.append(cset[i])

        return new_set

    '''
    Calcula os novos custos dado indices dos ultimos 2 elementos mais semelhantes
    old_cost: Antiga matriz de custo
    tidx_1: Indice do atributo alvo 1 agrupado
    tidx_2: Indice do atributo alvo 2 agrupado
    return: Nova matriz de custo
    '''
    def next_cost(self, old_cost, tidx_1, tidx_2, lowests):
        new_cost = []
        it = int(0)
        line_it = int(0)
        '''   
        # Corrigindo para que tidx_1 > tidx_2
        if tidx_1 < tidx_2:
            aux = tidx_1
            tidx_1 = tidx_2
            tidx_2 = aux
        '''
        # Unir linha idx_1 na idx_2. 
        line_toupdate = old_cost[tidx_2]
        line_toremove = old_cost[tidx_1]
        unified_line = []
        
        for el in line_toupdate:
            c = min([el, line_toupdate[it]])
            unified_line.append(c)
            it +=1

        for el in old_cost:
            if line_it > tidx_1:
                col_toremove = el[tidx_1]
                col_toupdate = el[tidx_2]

                #c = min(col_toupdate, col_toremove)
                c = min(col_toupdate, col_toremove)                   
                
                # Atualiza coluna
                el[tidx_2] = c

                # Remove coluna
                el.pop(tidx_1)
                    
            line_it += 1

        # Atualiza linha
        old_cost[tidx_1] = unified_line

        # Remove linha
        old_cost.pop(tidx_1)

        #Remove linha de minimos
        lowests.pop(tidx_1)
        
        new_cost = old_cost
        return new_cost
    
    '''
    Classificando de acordo com os agrupamentos
    group: Lista de grupos/conjuntos de elementos semelhantes
    '''
    def classify(self, group):
        predict = []
        cls = int(0)
        for same_set in range(len(group)):
            for el in group[same_set]:
                predict.append(cls)
            cls += 1
        return predict

    '''
    Inicia Lista de custos mínimos
    '''
    def init_lowests(self, cost):
        lowests = []
        row = int(0)
        col = int(0)
        min_el = cost[1][0]  # Primeiro elemento
        
        for line in cost:
            col = 0
            min_el = line[0]

            for el in line:
                
                if(el < min_el) & (row != col):
                    min_el = el
                    
                col += 1
                
            lowests.append(min_el)   # Salva valor do elemento minimo da linha
            row += 1

        return lowests


def plot_data(plt, pt, cls):
    colors = ['red', 'green', 'lightblue', 'pink', 'purple']
    
    # Se houver mais grupos do que cores pré-definidas
    groups = max(cls) + 1
    color_step = 1/groups 
    
    for p, c in zip(pt, cls):
        if c > 4:
            scale = color_step*(c-5)
            color = (scale, scale, scale)
            
        else:
            color = colors[c]
        plt.plot(p[0], p[1], marker = 'o', markersize=10, markeredgecolor = 'black', markerfacecolor=color)
            

if __name__ == '__main__':
    # time before
    tb = time.process_time()
    
    #fpath = 'test.txt'
    fpath = 'Aggregation.txt'
    predict = []
    groups = 5
    

    dt = begin(fpath)
    lk = Linkage([[x[0], x[1]] for x in dt], [y[2] for y in dt])

    # Agrupamento. Chamada principal
    rset, rcost = lk.group_all([[i] for i in range(lk.sz)], groups = groups)
    
    # Predicao
    predict = lk.classify(rset)

    # Time after
    ta = time.process_time()
    
    # Plot    
    plt.grid()
    plt.title("Quantidade de grupos: " + str(groups))
    plot_data(plt, [[x[0], x[1]] for x in dt], predict)
    plt.show()

    ttime = ta - tb
    print("Tempo total de processe de classificação:", ttime)

    print(predict)

