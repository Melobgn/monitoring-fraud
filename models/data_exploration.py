import pandas as pd

# Charger les données
df = pd.read_csv("../data/creditcard.csv")

# Aperçu des données
print("Shape du dataset :", df.shape)
print(df.head())

# Vérifier les proportions de la classe cible
class_counts = df['Class'].value_counts()
print("\nRépartition des classes :\n", class_counts)

# Calculer les pourcentages
print("\nPourcentage des classes :\n", class_counts / len(df) * 100)