# Unsupervised_Slinkage_e_Kmeans
Aprendizado não supervisionado com single linkage e kmeans

## Dados
Os dados já estão preparados no formato usado pelo algoritmo, sendo os dados em formato .txt onde
- 1ª e 2ª coluna contém valores de atributos
- 3ª coluna contém a correta classificação de grupo

## Kmeans
*fname* - define o nome do arquivo local contendo os dados brutos  
*groups* quantidade máxima de grupos que serão formados na clusterização  
*max_it* quantidade máxima de iterações que pode ocorrer

## Single Linkage
*fname* define o nome do arquivo local contendo os dados brutos  
*groups* quantidade máxima de grupos que serão formados na clusterização

## Dependencia
Matplotlib - Visualização gráfica da classificação

## Resultado
A saída no console é uma lista contendo a classificação do grupo de cada indivíduo. A ordem se mantém a mesma dada pelo *input*  
A imagen é uma representação gráfica dos grupos preditos. A estrela preta (no algoritmo KMeans) mostra a média atual do valor de cada grupo

### Exemplo gráfico
*Single Linkage*  
*fname = Aggregation.txt*  
*groups = 5*  
![Resultado Single Linkage](https://user-images.githubusercontent.com/38757175/189747340-0b1b5fe7-5d87-48ae-895a-e64545ab1e13.png)
