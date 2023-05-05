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
