# Optimal Portfolio — Piontek & Poulard

Un outil d'optimisation de portefeuille en Python permettant de construire et d'analyser un portefeuille d'actions personnalisé.

## Fonctionnalités
- Saisie des actions par TICKER ou ISIN
- 4 stratégies de pondération :
  - Pondération égale
  - Pondération par capitalisation boursière
  - Variance minimale
  - Rendement maximum (avec contrainte de pondération minimale)
- Conversion automatique des prix en EUR via les taux de change historiques
- Statistiques clés : rendement annualisé, variance, ratio de Sharpe, drawdown maximum
- Tableau d'investissement 
- Valeur finale du portefeuille et profit
- Comparaison visuelle avec le MSCI World 
- Option de redémarrage pour créer un nouveau portefeuille


## Utilisation

pip install -r requirements.txt

python3 main.py

Suivez les instructions dans la console pour construire votre portefeuille.

## Structure du projet

optimal_portfolio/
  main.py            
  datafetcher.py      
  portfolio/
    weigths.py       
  requirements.txt     
   README.md

## Limitations
- Le programme ne reconnait seulement des ISIN américaines

## Packages
- yfinance
- pandas
- numpy
- scipy
- matplotlib
- seaborn
- requests

