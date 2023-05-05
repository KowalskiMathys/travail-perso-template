# Définitions des concepts de base

## Règles du sudoku
Avant d’entrer dans les concepts de métaheuristique et autres concepts plus avancés, avant de voir en détail comment résoudre un sudoku à l’aide des métaheuristiques, il faut au préalable savoir ce qu’est un sudoku et comment ces derniers fonctionnent. Le mot sudoku est un mot provenant du japonais et signifie « chiffre unique ». Un sudoku est un jeu dont le but est de remplir une grille avec une série de chiffre de 1 à 9. Comme son origine étymologique l’indique, on ne peut pas remplir la grille de n’importe quelle façon. La grille est divisée en neuf grilles plus petites. Chacune des petites grilles est divisée en neuf cases. Un chiffre (de 1 à 9) ne peut pas se trouver plus d’une fois dans la même petite grille, colonne, ligne ou diagonal. Chaque grille, ligne et colonne doit être remplie avec les chiffres de 1 à 9. Une règle plus conventionnelle et tacite que les précédentes règles, mais tout aussi rependue, est qu’une bonne grille de sudoku ne comporte qu’une seule et unique solution. Bien que l’on utilise des chiffres, tout autres ensemble de formes ou symboles pourrait les remplacer. De surcroit, les chiffres n’ont nullement besoin d’être dans l’ordre (1-2-3-4-5-6-7-8-9), il est possible et même probable que les chiffres ne soit pas ordonnés arithmétiquement (3-2-6-8-7-9-1-4-5). 

```{figure} figures/sudokuexemple1.png
---
width: 100%
---
Illustration d'un sudoku. Image tirée de https://blogs.unimelb.edu.au/sciencecommunication/files/2016/10/sudoku-p14bi6.png
```

Pour ce projet personnel, nous utiliserons la variante et les règles telles que nous les avons énoncées, il est cependant intéressant de noter qu’il n’existe pas qu’une seule variante de sudoku. Certains sudoku vont de 0 à 8, d’autres utilisent des symboles plutôt que des chiffres. Parfois, l’on peut en trouver qui sont plus subtils, demandant une certaine combinaison ou créant un visuel une fois résolus. De surcroit, bien que les règles d’origine, tout comme les nôtres, ne soumettent pas les diagonales au même règles que les colonnes et lignes – c’est-à-dire, pas de doublons et des chiffres de 1 à 9 – certaines variantes le demandes explicitement. 


## Définition des concepts de métaheuristique
Il existe de nombreuses façons de résoudre un sudoku, la plus évidente étant de le faire manuellement. Dans le cadre de ce projet nous tout d’abord nous demander : « quelle autre façons y’a-t-il de résoudre un sudoku ? » Plusieurs méthodes de résolution s’offrent à nous mais celle qui nous intéressera tout le long de ce projet est une résolution par métaheuristique. C’est un sujet assez complexe et c’est pourquoi, avant de s’attaquer directement au vif de sujet, il est impératif d’expliciter les concepts relatifs aux métaheuristiques et autres concepts inhérents. 

Qu’est-ce qu’une métaheuristique ? Le mot métaheuristique vient du grec « méta » qui signifie « au-delà ». La deuxième partie du mot vient elle aussi du grec et signifie « trouver ». L’agréa de ces deux mots signifie donc « trouver au-delà » ou « trouver à un plus haut niveau ». Par conséquent, une métaheuristique est une méthode, un algorithme utilisé dans des problèmes d’optimisations. Une telle méthode est principalement utilisée dans la résolution d’un problème lorsque l’on ne connait pas de moyen plus efficace de résoudre ce problème. Cependant nous allons faire abstraction – du moins le long de ce chapitre – de cette dernière remarque étant donné que l’objectif réside plus dans la résolution du sudoku que dans l’optimisation de la recherche. 

Les métaheuristiques sont de manière générale des algorithmes de hasard itératifs. En d’autres termes plus accessibles : un algorithme de méta est un algorithme qui va utiliser l’aléatoire comme base de fonctionnement et s’en servir à son avantage. De plus, puisque l’on parle d’itératif, cela signifie que l’on va répéter plusieurs fois un même processus. Les métaheuristique sont donc des méthodes d’optimisation visant un optimum et qui cherchent à l’atteindre en changeant une variable à chaque itération à partir d’un état défini aléatoirement.

```{figure} figures/sudokumeta1.png
---
width: 100%
---
Résolution d'un sudoku par métaheuristique. Image tirée de https://www.semanticscholar.org/paper/A-Hybrid-Heuristic-Approach-for-the-Sudoku-problem-Musliu-Winter/ed376a033dbec049a4d62b0361a89805c075ae24 
```

Comme le montre bien l’image au-dessus, nous sommes passés d’un état à un autre en changeant une variable. Ici, le 1 et le 5 du premier bloc ont été inversés dans le but de se rapprocher de la solution. 

Comme dit précédemment, les métaheuristiques sont principalement utilisés pour résoudre des problèmes d’optimisation. Leur objectif est donc de trouver une solution optimale. Cette solution, cet optimum recherché, l’est de façon global ce qui signifie que c’est une des meilleurs solutions à un problème, une des solutions qui comporte le moins d’erreur ou de problèmes. Elles fonctionnent généralement par échantillonnage en partant d’un état 0 et en essayant de s’approcher d’une solution globale et optimal qui se rapproche le plus possible d’une solution parfaite. Dans certains cas ou certains problèmes, l’optimum trouvé ne sera qu’une approximation de la meilleur solution. Dans d’autres cas, l’optimum sera la solution attendue. Comme on peut l’observer sur l’image ci-dessous, les métaheuristiques cherchent à atteindre le haut de la courbe, le maximum global. Cela implique évidemment une fonction objective dont le maximum global sera la solution. 

```{figure} figures/hillclimbing.png
---
width: 100%
---
Fonction objective annotée. Illustration tirée de https://www.baeldung.com/cs/hill-climbing-algorithm
```

De plus, il existe deux grands type de métaheuristique. Deux grandes catégories qui ont une approche bien différente d’un problème. La première utilise une approche dite de parcours qui consiste à faire évoluer une solution à chaque itération. C’est sur cette optique que nous allons basé ce projet. De nombreuse méthodes utilisent cette notion de parcours. On peut citer le récuit simulé, la recherche avec taboo ou encore les méthodes de bruitage et celle que nous allons étudier, la méthode du hill-climbing. La deuxième approche que nous passons ici en revu fonctionne avec la notion de population. Cela consiste à manipuler un ensemble d’état, de solution en parallèle. Une telle approche est utilisé notamment par les algorithmes génétiques. 

```{figure} figures/metaoptiques.png
---
width: 100%
---
Deux approches des métaheuristiques. 
Illustration tirée de https://www.techno-science.net/illustration/Definitions/1200px/m/metaheuristic-parcours-population_80420613aa814653884a48b531f19e09.png 
```

L’optique (a) correspond effectivement à une approche par étude de population. Comme on peut l’observer sur le graphique, l’on étudie plusieurs solutions en parallèle. Comme vous pouvez l’imaginez, cela nécessite beaucoup plus de mémoire qu’une simple recherche locale. La deuxième méthode (b) est évidemment la recherche par parcours. On peut voir que les différents points rouge renvoie tous vers un autre point rouge contrairement à l’optique de population ou tous les points rouge ont été trouvés et analysés en même temps.

```{figure} figures/sudokumeta1.png
---
width: 100%
---
Résolution d'un sudoku par métaheuristique. Image tirée de https://www.semanticscholar.org/paper/A-Hybrid-Heuristic-Approach-for-the-Sudoku-problem-Musliu-Winter/ed376a033dbec049a4d62b0361a89805c075ae24 
```

## Différente notions de métaheuristique
Qu’est-ce que l’on entend par état exactement ? un état pourrait se caractériser dans notre cas comme une grille de sudoku quelconque. Prenons par exemple l’image de dessus et attribuons au premier sudoku le numéro 1. Cette grille est un état du sudoku en question, elle est certe erronée mais cela importe peu. Si l’on regarde la grille de droite, on s’aperçoit qu’elle ressemble énormément à la grille de gauche. Appelons la grille de droite la grille numéro 2. La seul différence notable entre 1 et 2 est que deux chiffres ont été inversés ce qui en fait deux grilles différentes et donc deux états différents. Voilà ce qu’est un état, c’est une instance du sudoku qui correspond à un remplissage possible de la grille. 

```{figure} figures/sudokuetat.png
---
width: 50%
---
Illustration d'un état dans le contexte du sudoku.
```

Typiquement, un état possible pourrait être celui-ci. La grille est complète, certe erroné mais du point de vue de l’algorithme, il reste une solution possible. 

Le principe général d’une méthode de métaheuristique consiste à partir de l’état N et de manipuler un ou plusieurs état proche (état N+1) et de sélectionner le meilleur état afin d’au fur et à mesure se rapprocher de la solution, de l’optimum. Plus explicitement, on commence à un état de base qui est une solution potentielle puisque chaque état représente une solution à la différence que ces solutions sont pour la plupart fausses ou plutôt insatisfaisantes. Dans le cas d’un sudoku, il existe un nombre presque illimité de solution – environ 6 671 milliards de milliards de grilles – mais une seule d’entre elle est satisfaisante, toutes les autres sont erronées. 

A partir de l’état de base, l’on va observer des états voisins, des états obtenus en effectuant un certain nombre de modification sur l’état actuel. La suite est plus complexe puisqu’elle consiste à sélectionner un des états afin de recommencer le processus, cependant cela implique que pour se rapprocher de la solution il faut sélectionner le bon état, c’est sur cette étape que la plupart des métaheuristiques se différencient : Quel état voisin est le bon choix ? L’objectif est donc de passer d’état insatisfaisant à un état satisfaisant, voire à l’état et les états les plus satisfaisants, c’est-à-dire la solution.

A noter qu’un problème possède peut-être plusieurs états satisfaisants dépendant du problème, de l’objectif recherché et par conséquent de ce que l’on appelle un critère d’arrêt. Un critère d’arrêt est un critère que l’on va donner à l’algorithme afin qu’il sache quand s’arrêter. Ce critère peut être un temps d’exécution comme un niveau d’optimisation ou de précision demandé. Par exemple : il serait envisageable, quoique que quelque peu diminué de sens, de définir notre critère d’arrêt à 4 faute prêt. C’est-à-dire de définir la solution satisfaisant d’un sudoku comme une solution qui ne possède que 4 erreurs ou moins.  Dans ce cas le critère d’arrêt serait en rapport avec la fonction heuristique. Dans le cas ou l’on définit le critère d’arrêt par rapport à un nombre d’erreur cela implique que la fonction soit basé sur le nombre d’erreur comme on peut le voir sur l’image ci-dessous. Nous étudierons cette fonction plus en profondeur dans les chapitres qui suivent.

```{figure} figures/sudokuetat.png
---
width: 50%
---
Illustration d'un état dans le contexte du sudoku.
```

Si le critère d’arrêt est un élément important de la résolution, la définition du champ de voisinage l’est tout autant. En effet, si l’on demande à l’algorithme de balayer un nombre trop petit de voisin, il est possible que l’on ne progresse que peu rapidement ou pire que l’on tombe dans un optimum local, c’est-à-dire une solution qui serait la meilleur d’après son voisinage mais qui n’est de loin pas l’optimum global, il se peut même que cet optimum local ne satisfasse pas le critère d’arrêt. 

En plus du critère d’arrêt et du voisinage, les métaheuristiques ont également d’autres notions prépondérantes, à savoir : la mémoire et l’apprentissage, l’intensification ou l’exploitation, et enfin, la diversification ou l’exploration. La mémoire permet à l’algorithme d’ « apprendre » et permet de ne pas perde de temps sur des zones ou l’optimum global n’a aucune chance de se trouver. On peut parler de mémoire à court terme lorsque l’algorithme évite de repasser par des états déjà visité. Pour ce qui est de l’intensification, cela consiste à utiliser la mémoire afin de définir des zones intéressantes à explorer. Pour finir, la diversification désigne le fait de récolter des données sur le problème en cours. La plupart du temps, ces différentes variables sont liées les unes aux autres et toute la complexité d’une optimisation méta réside dans le fait d’équilibré (ou non) ces différent aspect de l’algorithme. 