# Analyse de l’implémention
Malheureusement, nous savions qu’il était probable que la fonction se bloque dans un optimum local et c’est ce qui arrive constamment. Même si l’implémentation ne parvient pas à trouver une solution parfaite, elle s’en approche étonnamment près si l’on regarde les différents scores. De plus voici quelque graphique dénotant de la performance de l’algorithme a trouver la solution. On peut observer que le score moyen tourne autour des 220.

```{figure} figures/Figure_1.png
---
width: 70%

```


Bien que l’on recommence plusieurs fois le hillclimbing afin de se rapprocher de la solution, on peut observer que cela ne crée pas une grande différence a cette échelle.
Certainement que si l’on testait de recommencer à diffèrent endroit une centaine de fois plutôt qu’une dizaine pourrait-on voir une évolution. Je ne recommande cependant pas de faire cela car le programme commencera certainement à faire peinez votre ordinateur passé les 50 itérations.

```{figure} figures/Figure_1a.png
---
width: 50%

```
```{figure} figures/Figure_1b.png
---
width: 50%

```

## Code python complet
```python
import numpy as np
import sys
import matplotlib.pyplot as plt

class Sudoku():

	def __init__(self):
		self.reset()

	def reset(self):
		# la méthode va créer des liste de liste de 1 à 9 et permuter ses nombres entre eux
        # 
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
	
	def printBoard(self, board=[]):
		#c'est dans le nom lol
		if(board == []):
			board = self.board
		
		for i in range(len(board)):
			if(i % 3 == 0 and i != 0):
				print("------+------+------")
			for j in range(len(board[i])):
				if(j % 3 == 0 and j != 0):
					sys.stdout.write("|")
				sys.stdout.write(str(board[i][j]) + " ")
			print("")

	def swapToPlace(self, val, line, col):
		# npwhere va renvoyer la position de la valeur fixe
        # puis on va echanger la place de cette valeur fixe a l'endroit ou elle doit être
		valIndex = np.where(self.board[line]==val)[0][0]
		self.swap(self.board[line], valIndex, col)

	def setup(self):
		# la méthode sert à placer les cases fixes au bon endroit
		for (val, row, col) in self.fixedValues:
			self.swapToPlace(val, row, col)

	def fitness(self, board=[]):
		# la fonction agit sur le self.board  et va compter le nombre de chiffre unique (qui ne se trouve qu'une  fois dans row, colonne et grille de 3x3)
		# 
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

	def swap(self, arr, pos1, pos2):
		# la méthode échange deux chiffre d'une grille
		arr[pos1], arr[pos2] = arr[pos2], arr[pos1]

	def isFixed(self, row, col):
		# la fonction vérifie simplement si un chiffre est fixe
		for t in self.fixedValues:
			if(row == t[1] and col == t[2]):
				return True
		return False

	def bestNeighbor(self):
		# on commence par faire une copie de la grille dans tempboard
		# i = ligne j et k vont être des colonnes
		# i et j sont un chiffre et i et k un autre
		# on a donc deux chiffre -> on regarde si ils sont fixe et si non, on les swap
		# on enregistre le swap dans contestant (ligne, col1 col2, score)
		# on regarde qui a le meilleur score entre contestant et best
		# si contestant est mieux que best on enregistre contestant dans best et on recommence
		# a la fin cela permet de renvoyer le meilleur voisin (best)
		tempBoard = self.board.copy()
		# best = (row, (col1, col2), val)
		# col1 e col2 serão trocadas com o swap.
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
					#Desfaz o swap para poder reutilizar o tabuleiro
					self.swap(tempBoard[i], j, k)
		return best

	def climbHill(self):
		# calculer nombre de truc bon
		# tenir une liste des différent scores
		# on regard quel est le meilleur voisin
		# si le score du voisin nextscore est moins bien que maxscore alors on a trouvé la meilleur solution
		# sinon on échange la grille acutelle avec la grille voisine et on recommence
		scores = []
		maxScore = self.fitness()
		# print("Initial score: " + str(maxScore))
		while True:
			# print("Current score: " + str(maxScore))
			scores.append(maxScore)
			(row, (col1, col2), nextScore) = self.bestNeighbor()
			if(nextScore <= maxScore):
				return scores
			self.swap(self.board[row], col1, col2)
			maxScore = nextScore 

sud = Sudoku()
print("Hill Climbing")
print("Plus le score est élevé, mieux c'est. (Max = 243)")
print("Le score reflète le nombre de valeurs uniques par ligne, colonne et quadrant.")
trials = []
maxScore = -1
bestBoard = []
# on va tenter 10 fois l'expérience et voir comment ça va et la quelle est la meilleur
# une fois qu'on a le meilleur score il suffit d'acceder a la grille correspondant
for i in range(5):
	sud.reset()
	finalScore = sud.climbHill()
	maxFinalScore = max(finalScore)
	if(maxScore < maxFinalScore):
		maxScore = maxFinalScore
		bestBoard = sud.board.copy()
	print(str(i) + ") " + str(finalScore[-1]) + "/243")
	if(finalScore == 243):
		print("SOLUÇÃO CORRETA!")
		sud.printBoard()
		break
	trials.append(finalScore)
	# print(finalScore)
print("Melhor pontuação: %i" % maxScore)
sud.printBoard(bestBoard)


#Desenha um gráfico do desempenho de cada execução do hill climbing
for trial in trials:
	plt.plot(trial)
plt.title('Hill Climbing')
plt.ylabel('Ponctuation (Max 243)')
plt.xlabel('itérations')
plt.show()
```
