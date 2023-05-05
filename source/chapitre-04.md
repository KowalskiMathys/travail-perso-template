# présentation de l’implémentation python
Il est à présent temps de voir ce que cela donne en python. Plus précisément ce chapitre est dédié a la présentation et a l’explication d’une implémentation python. Cette implémentation en python de Hill climbing sert à résoudre des sudoku. Bien que le code à été commentez en français, l’implémentation d’origine n’est pas de moi mais est trouvable sur le dépôt https://github.com/GuilhermeFreire/Sudoku_Gen_Alg/blob/master/hill_climbing.py 

Cette implémentation nécessite l’aide des modules numpy, sys, matplotlib.pyplot qu’il faut donc importer en premier lieu. Le module le plus important est numpy car c’est de lui que viennent de nombreuse fonction mathématique utiliser dans cette implémentation. Quant aux deux autres modules, ils servent uniquement à afficher le sudoku ainsi que les données récolté par le programme.

```python
import numpy as np
import sys
import matplotlib.pyplot as plt
```

## Création du sudoku
Afin de créer le sudoku et d’appliquer une métaheuristique dessus, on va créer une classe `Sudoku` qui va être le support des méthodes de hill climbing et relatives au sudoku. La première chose que l’on souhaite faire lorsque l’on crée une instance de cette classe, c’est évidemment créer un sudoku. C’est pourquoi l’on va au sein du constructeur appelé la méthode `reset()` qui aura pour effet de créer un sudoku sous forme de liste de liste.

```python
class Sudoku():
	def __init__(self):
		self.reset()
```
### la méthode de réinitialisation
Premièrement, on pourrait se demander pourquoi la méthode `reset` s’appelle ainsi. C’est car elle va plus tard servir à réinitialiser le sudoku afin de recommencer le hill climbing à partir d’un autre état. Cela permet par exemple d’obtenir une meilleur solution sans se retrouver coincé dans un optimum local. Pour ce qui est du fonctionnement de la méthode, elle se présente comme ceci : 

```python
	def reset(self):
		self.board = (np.indices((9,9)) + 1)[1]
		for i in range(len(self.board)):
			self.board[i] = np.random.permutation(self.board[i])
		self.fixedValues = np.array([
			#(val, row, col)
			(7, 0, 3),
			(1, 1, 0),
			(4, 2, 3),
			(3, 2, 4),
			(2, 2, 6),
			(6, 3, 8),
			(5, 4, 3),
			(9, 4, 5),
			(4, 5, 6),
			(1, 5, 7),
			(8, 5, 8),
			(8, 6, 4),
			(1, 6, 5),
			(2, 7, 2),
			(5, 7, 7),
			(4, 8, 1),
			(3, 8, 6)
			])
		self.setup()
```
La méthode va commencer par créer une grille de sudoku sous forme d’array (un array ressemble énormément à une liste si ce n’est qu’un array ne contient que des éléments du même type). Le fait de représenter un sudoku sous forme d’array s’apparente à leur faire sous forme de liste de liste. Au commencement, les array seront triés et le sudoku ressemble à ceci : 

`array([1, 2, 3, 4, 5, 6, 7, 8, 9]), array([1, 2, 3, 4, 5, 6, 7, 8, 9]), array([1, 2, 3, 4, 5, 6, 7, 8, 9]), array([1, 2, 3, 4, 5, 6, 7, 8, 9]), array([1, 2, 3, 4, 5, 6, 7, 8, 9]), …, array([1, 2, 3, 4, 5, 6, 7, 8, 9]).`

Par la suite la méthode va donc permuter de manière aléatoire les chiffres dans leur arrays respectifs. Si vous observez la méthode, vous pouvez remarquez qu’une grande place est occupé par un array. Il s’agit des valeurs fixe du sudoku, il s’agit en réalité des chiffres qui ne bouge pas et sont déjà présent sur le sudoku avant que vous ne le commenciez. Evidemment, puisque ces chiffres sont définis d’avance, cette implémentation ne travaille que sur un sudoku en particulier. Mais il est tout a fait possible de changer le sudoku en changer les valeurs fixe dans les tuples. La première valeurs correspond au chiffre, la deuxième à la ligne et la troisième à la colonne. 

Que fait-on de ces valeurs fixe ? En effet, pour le moment nous n’avons qu’une liste de valeur fixe ainsi qu’une grille de 9x9 désordonné. Comment va on passer d’une grille aux chiffres aléatoire à une grille de sudoku contenant des valeurs fixe ? Grâce à la méthode `setup`.

#### les méthodes relatives au sudoku
Par la suite, plusieurs méthode sont nécessaire, la méthode `setup` qui va appeler la méthode `swapToPlace` qui elle-même va appeler la méthode `swap`. Commençons par la dernière méthode et remontons le code. La méthode `swap` comme son nom l’indique va échanger – swap – deux chiffres sur la grille. Elle est assez simple à appréhender, c’est pourquoi je vous propose de jeter un coup d’œil par vous-même, arr correspond à l’array (la ligne) et pos1 et pos2 sont les positions à échanger. 

```python
	def swap(self, arr, pos1, pos2):
		arr[pos1], arr[pos2] = arr[pos2], arr[pos1]
```

Cette méthode est appelé au sein de la méthode `swapToPlace`. Cette dernière sert à placer une valeur de la grille à un endroit précis. Lorsque cette méthode est appelée, la grille n’est pas trié et la valeur fixe peut se trouver à n’importe quelle position sur la ligne. Il faut donc trouver où se trouve la valeur et l’enregistrer dans `valIndex`. Une fois que l’on connait la position de la valeur, on peut la replacer au bon endroit avec `swap`.

```python
	def swapToPlace(self, val, line, col):
		valIndex = np.where(self.board[line]==val)[0][0]
		self.swap(self.board[line], valIndex, col)
``` 

À la fin de `reset` la méthode `setup` est appelée, cette méthode va servir à préparer le sudoku, c’est-à-dire à placer les valeurs fixes au bon endroit sur la grille. Cette méthode est également aisée à comprendre, il s’agit d’une simple boucle qui appelle la méthode `swapToPlace` en entrant en paramètre les informations des valeurs fixe. 

```python
	def setup(self):
		for (val, row, col) in self.fixedValues:
			self.swapToPlace(val, row, col)
```
## Implémentation de Hill climbing
La encore, l’implémentation se décompose en plusieurs méthodes. Afin de pouvoir résoudre un sudoku grâce au métaheuristique, il faut plusieurs moyen : une méthode capable de déterminer le « score » d’une solution. Cette méthode répond à la question : « Cet état est-il proche de l’optimum ? ». Il faut également une méthode qui va discriminer entre les solutions afin de retourner le meilleur voisin. Et finalement, il faut une méthode principale qui recommencer le processus encore et encore jusqu’à trouver un optimum local ou global. A noter, que dans ce cas, le critère d’arrêt est rempli lorsque l’on a atteint un optimum. Ces trois méthodes seront respectivement nommées `fitness`, `bestNeighbor` et `climHill`.

### Cet état est-il proche de l’optimum ?
Afin de répondre à cette question, on va créer une méthode `fitness` qui prend en paramètre optionnel une grille de sudoku. Si ce paramètre n’est pas remplis, alors il s’en suivra que la grille sera la grille actuelle. Cette méthode sera utile pour choisir le meilleur voisin. Afin de déterminer quel voisin est le meilleur, il faut un moyen de classer, de trier, ces voisin. Nous l’avons déjà vu plus tôt dans ce projet, il existe deux façon de trier les voisins : par nombre de chiffre qui pose problème ou par nombre de chiffre qui sont valide. C’est la deuxième approche qui est utiliser dans cette implémentation. Les voisins seront ordonné selon leur score. Le meilleur score, celui de la véritable solution, est de 243. Il s’agit en réalité de 81 + 81 + 81 car l’on va compter le nombre de chiffre valide par colonne, ligne et grille de 3x3. Le maximum que l’on puissent obtenir pour les grille de 3x3 est 81 car il y a 9 chiffre possiblement valide et il y a 9 grilles. De même pour les lignes et colonnes, il y a 9 chiffres par ligne/colonne et il y a 9 lignes/colonnes. Ce qui nous fait un total de 81. 
Le code de la méthode `fitness` est donc le suivant :
```python
	def fitness(self, board=[]):
		if(board == []):
			board = self.board
		score = 0
		rows, cols = board.shape
		for row in board:
			score += len(np.unique(row))
		for col in board.T:
			score += len(np.unique(col))
		for i in range(0, 3):
			for j in range(0, 3):
				sub = board[3*i:3*i+3, 3*j:3*j+3]
				score += len(np.unique(sub))
		return score
```
Vous pouvez également remarquez que l’on définit board comme liste vide et non comme self.board. Cela est du au fait qu’on ne peut pas faire référence à `self` puisqu’il n’a pas encore été pris en paramètre dans la méthode. Cette méthode , nommez fitness par son créateur qui de toute évidence avait un certain sens de l’humour, est globalement composé de trois parti principales. La première est une boucle qui va compter le nombre de valeurs valide par lignes et les ajouter au score. La deuxième fait de même avec les colonnes. Et la troisième compte le nombre de valeurs valides par grilles de 3x3.
### Quel est le meilleur voisin ?
Nous avons à présent un moyen de calculer le score d’une solution. Il nous faut à présent une méthode qui va analyser le voisinage. C’est précisément le but de la méthode `bestNeighbor`. Elle fonctionne ainsi : on commence par faire une copie de la grille dans `tempBoard`. Cela permet de travailler sur la copie et non sur la solution de base. On évite ainsi de remplacer la grille actuelle par une grille moins bonne. Ce qui suit demande un peu plus d’effort de compréhension et pourrait certainement être retravaillée. Comme vous pouvez le voir sur la méthode, on va procéder en faisant une première boucle où `i` correspond aux lignes de la grille, puis une deuxième boucle, interne à la première où `j` correspond aux colonnes de la grille. Jusque là c’est assez compréhensible. On va finalement effectuer une troisième boucle à l’intérieur de la deuxième où `k` correspond également à une colonne. 

Cependant, il y a une différence majeure. Là ou `j` va de 0 à 8, `k`, lui, dépend de `i` puisqu’il va de `i` à 8. Cela permet de ne pas répéter des opérations déjà effectué. Puisque l’on va passer en revue chaque valeurs se trouvant dans la grille, il est tout à fait logique que l’on tombe sur une valeur fixe. Pour s’éviter des calculs inutiles (il ne sert à rien de regarder l’effet qu’un échange pourrait avoir puisque ces valeurs ne peuvent être échangées), la méthode va vérifier si une des deux valeurs (la valeurs se trouvant à la position (i,j) et celle se trouvant à la position (i,k)) est fixe. Le cas échéant, on va simplement passer par-dessus les opérations qui suivent. Mais si au contraire, les valeurs sont échangeables, alors on va les échanger créant ainsi une solution voisine. Il s’agit ensuite simplement de comparer le score du voisin nouvellement créé et du voisin précédemment enregistré comme meilleur voisin dans `best`.
```python
	def bestNeighbor(self):
		tempBoard = self.board.copy()
		best = (0, (0,0), -1)
		for i in range(len(tempBoard)):
			for j in range(len(tempBoard[i])):
				for k in range(i,len(tempBoard)):
					if(self.isFixed(i,j) or self.isFixed(i,k)):
						continue
					self.swap(tempBoard[i], j, k)
					contestant = (i, (j,k), self.fitness(tempBoard))
					if(contestant[2] > best[2]):
						best = contestant
					self.swap(tempBoard[i], j, k)
		return best
```
### Puis-je trouver une meilleur solution ?
Finalement, la réponse à cette question se trouvera dans la méthode principal du hill climbing, c’est-à-dire `climbHill`. Dans l’objectif de « grimper la colline », il est nécessaire de pouvoir effectivement se rapprocher du sommet (la solution) à chaque étapes. On va donc enregistré le score de la solution actuel dans `maxScore`. Dans un autre objectif, on va également enregistré les différents scores dans une liste afin de pouvoir analyser les données le moment venu. La suite est une simple boucle `while True` qui va simplement appelé la méthode `bestNeighbor` et comparé le score du meilleur voisin avec le score actuelle. S’il s’avère que la solution actuelle possède le meilleur score, la méthode se termine et il suffira d’accéder à la grille correspondante. Au contraire, si la solution voisine est meilleure, alors on va remplacer la solution actuelle par l’état voisin. Vous connaissez la suite, on continue ainsi jusqu’à trouver un optimum.
```python
	def climbHill(self):
		scores = []
		maxScore = self.fitness()
		while True:
			scores.append(maxScore)
			(row, (col1, col2), nextScore) = self.bestNeighbor()
			if(nextScore <= maxScore):
				return scores
			self.swap(self.board[row], col1, col2)
			maxScore = nextScore
```

