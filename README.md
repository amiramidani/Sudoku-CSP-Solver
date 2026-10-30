# 🧩 Sudoku CSP Solver
### Intelligence Artificielle | Artificial Intelligence | Python

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Artificial Intelligence](https://img.shields.io/badge/Artificial_Intelligence-CSP-purple)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![Project](https://img.shields.io/badge/Project-Academic-orange)

**🇫🇷 Français | 🇬🇧 English**

---


## 📌 Présentation du projet

**Sudoku CSP Solver** est un projet académique d'intelligence artificielle développé en Python.

Il consiste à résoudre automatiquement des grilles de Sudoku en utilisant les **problèmes de satisfaction de contraintes (CSP – Constraint Satisfaction Problems)**.

Le projet met en œuvre plusieurs techniques d'intelligence artificielle afin d'optimiser la recherche de solutions et de comparer les performances des algorithmes.

L'objectif est de démontrer comment la propagation des contraintes et les heuristiques de recherche permettent d'améliorer l'efficacité d'un solveur de Sudoku.

## 🎯 Objectifs du projet

- Modéliser le Sudoku comme un problème CSP.
- Implémenter un algorithme de résolution automatique.
- Utiliser le Backtracking pour rechercher les solutions.
- Optimiser la résolution grâce aux heuristiques intelligentes.
- Appliquer la propagation des contraintes avec AC-3.
- Comparer les performances de différentes stratégies.
- Analyser le temps d'exécution et la complexité de recherche.

## 🧠 Algorithmes et techniques utilisés

| Algorithme | Description |
|---|---|
| Backtracking | Recherche récursive avec retour en arrière lorsqu'une solution partielle est invalide. |
| MRV | Sélectionne la variable possédant le moins de valeurs possibles. |
| Degree Heuristic | Privilégie les variables impliquées dans le plus grand nombre de contraintes. |
| LCV | Choisit la valeur qui limite le moins les possibilités des autres variables. |
| Forward Checking | Élimine les valeurs incompatibles après chaque affectation. |
| AC-3 | Réduit les domaines des variables grâce à la cohérence des arcs. |

Ces techniques permettent de réduire l'espace de recherche et d'améliorer l'efficacité de la résolution.

## 🚀 Fonctionnalités principales

- Résolution automatique de grilles Sudoku.
- Prise en charge des grilles 4×4, 9×9 et 16×16.
- Modélisation CSP.
- Backtracking optimisé.
- Propagation des contraintes.
- Assistant interactif en ligne de commande.
- Comparaison des performances des algorithmes.
- Mesure du temps d'exécution.
- Analyse du nombre de nœuds explorés et de retours en arrière.
- Comparaison facultative avec Google OR-Tools.

## 🛠️ Technologies utilisées

- **Langage :** Python 3
- **Domaine :** Intelligence artificielle
- **Approche :** Constraint Satisfaction Problems (CSP)
- **Algorithmes :** Backtracking, MRV, LCV, AC-3
- **Bibliothèque facultative :** Google OR-Tools
- **Interface :** Ligne de commande (CLI)

## 📂 Structure du projet

```text
Sudoku-CSP-Solver/
│
├── projet1.py
├── ds1 (1).pdf
└── README.md
```

**Description des fichiers :**

- `projet1.py` : code source Python du solveur Sudoku.
- `ds1 (1).pdf` : présentation académique du projet.
- `README.md` : documentation du projet.

## 💻 Installation et exécution

### 1. Cloner le projet

```bash
git clone https://github.com/amiramidani/Sudoku-CSP-Solver.git
```

### 2. Accéder au dossier

```bash
cd Sudoku-CSP-Solver
```

### 3. Exécuter le programme

```bash
python projet1.py
```

### 4. Résoudre une grille spécifique

```bash
python projet1.py --size 9
```

Autres tailles disponibles :

```bash
python projet1.py --size 4
python projet1.py --size 16
```

### 5. Lancer l'assistant interactif

```bash
python projet1.py --assistant
```

### 6. Comparer les performances

```bash
python projet1.py --bench
```

### 7. Afficher les étapes de résolution

```bash
python projet1.py --trace
```

### 8. Installer OR-Tools (facultatif)

```bash
pip install ortools
```

## 📊 Analyse des performances

Le projet compare trois configurations :

| Configuration | Techniques |
|---|---|
| Naive | Backtracking classique |
| Optimized | MRV + Forward Checking + LCV |
| Advanced | MRV + Forward Checking + LCV + AC-3 |

**Indicateurs étudiés :**

- Temps d'exécution.
- Nombre de nœuds explorés.
- Nombre de retours en arrière.
- Nombre de valeurs éliminées par AC-3.
- Vérification de la solution.

Cette analyse permet d'évaluer l'impact des heuristiques et de la propagation des contraintes sur les performances.

## 🎓 Compétences développées

- Intelligence artificielle
- Programmation Python
- Conception d'algorithmes
- Résolution de problèmes CSP
- Backtracking et récursivité
- Optimisation algorithmique
- Analyse des performances
- Résolution de problèmes complexes
- Travail collaboratif

## 👩‍💻 Équipe du projet

Ce projet a été réalisé par :

- **Amira Midani**
- **Eya Ibn Abdelhedi**
- **Gofrane Araar**

## 📚 Contexte académique

**Projet :** Résolution du Sudoku par satisfaction de contraintes

**Sujet :** Topic 3 – Sudoku CSP

**Année universitaire :** 2025–2026

---

## 📌 Project Overview

**Sudoku CSP Solver** is an academic Artificial Intelligence project developed in Python.

The project focuses on solving Sudoku puzzles automatically using **Constraint Satisfaction Problems (CSP)**.

It implements several artificial intelligence techniques to optimize the search process and compare algorithmic performance.

The main objective is to demonstrate how constraint propagation and intelligent search heuristics can improve Sudoku-solving efficiency.

## 🎯 Project Objectives

- Model Sudoku as a Constraint Satisfaction Problem.
- Implement an automatic Sudoku solver.
- Apply recursive Backtracking.
- Optimize the solving process using intelligent heuristics.
- Implement constraint propagation with AC-3.
- Compare different solving strategies.
- Analyze execution time and search complexity.

## 🧠 Algorithms and Techniques

| Algorithm | Description |
|---|---|
| Backtracking | Recursive search that reverses decisions when a partial solution is invalid. |
| MRV | Minimum Remaining Values: selects the variable with the fewest legal values. |
| Degree Heuristic | Prioritizes variables involved in the largest number of constraints. |
| LCV | Least Constraining Value: selects values that restrict neighboring variables the least. |
| Forward Checking | Removes incompatible values after each assignment. |
| AC-3 | Enforces arc consistency to reduce variable domains. |

These techniques reduce the search space and improve solving efficiency.

## 🚀 Key Features

- Automatic Sudoku puzzle solving.
- Support for 4×4, 9×9 and 16×16 grids.
- CSP-based problem modeling.
- Optimized Backtracking.
- Constraint propagation.
- Interactive command-line assistant.
- Algorithm performance comparison.
- Execution time measurement.
- Search node and backtracking analysis.
- Optional comparison with Google OR-Tools.

## 🛠️ Technologies Used

- **Programming Language:** Python 3
- **Field:** Artificial Intelligence
- **Approach:** Constraint Satisfaction Problems
- **Algorithms:** Backtracking, MRV, LCV, AC-3
- **Optional Library:** Google OR-Tools
- **Interface:** Command-Line Interface (CLI)

## 📂 Project Structure

```text
Sudoku-CSP-Solver/
│
├── projet1.py
├── ds1 (1).pdf
└── README.md
```

**File descriptions:**

- `projet1.py`: Main Python implementation.
- `ds1 (1).pdf`: Academic project presentation.
- `README.md`: Project documentation.

## 💻 Installation and Usage

### 1. Clone the Repository

```bash
git clone https://github.com/amiramidani/Sudoku-CSP-Solver.git
```

### 2. Navigate to the Project

```bash
cd Sudoku-CSP-Solver
```

### 3. Run the Program

```bash
python projet1.py
```

### 4. Solve a Specific Sudoku Grid

```bash
python projet1.py --size 9
```

Other supported grid sizes:

```bash
python projet1.py --size 4
python projet1.py --size 16
```

### 5. Launch the Interactive Assistant

```bash
python projet1.py --assistant
```

### 6. Compare Algorithm Performance

```bash
python projet1.py --bench
```

### 7. Display the Solving Process

```bash
python projet1.py --trace
```

### 8. Install OR-Tools (Optional)

```bash
pip install ortools
```

## 📊 Performance Evaluation

The project compares three configurations:

| Configuration | Techniques |
|---|---|
| Naive | Basic Backtracking |
| Optimized | MRV + Forward Checking + LCV |
| Advanced | MRV + Forward Checking + LCV + AC-3 |

**Performance indicators:**

- Execution time.
- Number of explored nodes.
- Number of backtracks.
- Number of domain values removed by AC-3.
- Solution verification.

This evaluation highlights how intelligent heuristics and constraint propagation influence computational efficiency.

## 🎓 Skills Demonstrated

- Artificial Intelligence
- Python Programming
- Algorithm Design
- Constraint Satisfaction Problems
- Recursive Backtracking
- Algorithm Optimization
- Performance Analysis
- Computational Problem-Solving
- Team Collaboration

## 👩‍💻 Project Team

This academic project was collaboratively developed by:

- **Amira Midani**
- **Eya Ibn Abdelhedi**
- **Gofrane Araar**

## 📚 Academic Context

**Project:** Sudoku Solver Using Constraint Satisfaction Problems

**Topic:** Topic 3 – Sudoku CSP

**Academic Year:** 2025–2026

---

## 📬 Contact / Contact

**Amira Midani**

Computer Science and Information Systems Student

**GitHub:** [amiramidani](https://github.com/amiramidani)

---

⭐ **FR :** N'hésitez pas à explorer le code source et la documentation du projet.

⭐ **EN:** Feel free to explore the source code and project documentation.
