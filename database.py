import sqlite3

import csv
class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name + ".db")
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, column_definitions):
        if self.conn is None:
            raise ValueError("Base de données non créée")

        # Vérification des types de données et des noms de colonnes
        for column_name, column_type in column_definitions.items():
            if not isinstance(column_name, str) or not isinstance(column_type, str):
                raise ValueError("Les noms de colonnes et les types de données doivent être des chaînes de caractères")

        # Construction de la requête SQL pour créer la table
        columns = []
        for i, (column_name, column_type) in enumerate(column_definitions.items()):
            if i == 0:  # Première colonne est la clé primaire
                columns.append(f"{column_name} INTEGER PRIMARY KEY AUTOINCREMENT")
            else:
                columns.append(f"{column_name} {column_type}")
        columns_str = ', '.join(columns)
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"

        # Affichage de la requête SQL pour débogage

        # Exécution de la requête SQL
        try:
            self.cursor.execute(query)
            self.conn.commit()
            print(f"Création de la table {table_name} dans la base de données {self.db_name}...")
        except sqlite3.Error as e:
            print(f"Erreur lors de la création de la table {table_name} : {e}")

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            print(f"Fermeture de la connexion à la base de données {self.db_name}...")

    def search(self, table_nom, colonne_nom, valeur):
        # Créer la requête SQL pour rechercher les données
        query = f"SELECT * FROM {table_nom} WHERE {colonne_nom} LIKE '%{valeur}%'"

        # Exécuter la requête SQL
        try:
            self.cursor.execute(query)
            résultats = self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erreur lors de la recherche : {e}")
            return

        # Afficher les résultats
        if résultats:
            print(f"\nRésultats de la recherche dans la table {table_nom} :")
            colonnes = self.get_columns(table_nom)
            print("+" + "-" * 40 + "+")
            print("|", end="")
            for colonne in colonnes:
                print(f"{colonne:<10}", end="|")
            print()
            print("+" + "-" * 40 + "+")
            for ligne in résultats:
                print("|", end="")
                for valeur in ligne:
                    print(f"{valeur:<10}", end="|")
                print()
            print("+" + "-" * 40 + "+")
        else:
            print(f"Aucun résultat trouvé dans la table '{table_nom}' ")
        return []       
                # def search(self, table_nom, colonne_nom, valeur):
                # query = f"SELECT * FROM {table_nom} WHERE {colonne_nom} LIKE ?"
                # self.cursor.execute(query, (f"%{valeur}%",))
                # return self.cursor.fetchall()

    def delete(self, table_nom, id):
        query = f"DELETE FROM {table_nom} WHERE id = ?"
        self.cursor.execute(query, (id,))
        self.conn.commit()

    def read(self):
        table_nom = input('entrer le nom de la table : ')

        # Récupérer les données de la table
        données = self.get_data(table_nom)

        # Afficher les données
        if données:
            print(f"\nDonnées de la table {table_nom} :")
            print("+" + "-" * 58  + "+")
            colonnes = self.get_columns(table_nom)
            print("|", end="")
            for colonne in colonnes:
                print(f"{colonne:<10}", end="|")
            print()
            print("+" + "-" * 58 + "+")
            for ligne in données:
                print("|", end="")
                for valeur in ligne:
                    print(f"{valeur:<10}", end="|")
                print()
            print("+" + "-" * 58 + "+")
        else:
            print(f"Aucune donnée trouvée dans la table {table_nom}")

    def get_data(self, table_nom):
        self.cursor.execute(f"SELECT * FROM {table_nom}")
        return self.cursor.fetchall()

    def insert_data(self, table_nom, valeurs):
        # Récupérer les colonnes de la table
        colonnes = self.get_columns(table_nom)

        # Identifier la colonne de la clé primaire
        primary_key_column = colonnes[0]

        # Supprimer la colonne de la clé primaire des valeurs à insérer
        valeurs.pop(primary_key_column, None)

        # Créer la requête SQL pour insérer les données
        columns = ', '.join(valeurs.keys())
        placeholders = ', '.join(["?"] * len(valeurs))
        requete = f"INSERT INTO {table_nom} ({columns}) VALUES ({placeholders})"

        # Exécuter la requête SQL
        self.cursor.execute(requete, list(valeurs.values()))
        self.conn.commit()

    def get_columns(self, table_nom):
        # Créer la requête SQL pour récupérer les colonnes de la table
        requete = f"PRAGMA table_info({table_nom})"

        # Exécuter la requête SQL
        self.cursor.execute(requete)
        colonnes = [ligne[1] for ligne in self.cursor.fetchall()]    
        return colonnes   

    def update(self, table_nom):
        # Récupérer le nom de la colonne clé primaire
        primary_key_column = self.get_columns(table_nom)[0]

        # Demander à l'utilisateur de saisir l'ID de la donnée à mettre à jour
        id_a_modifier = int(input(f"Entrez l'{primary_key_column} de la donnée à mettre à jour : "))

        # Rechercher la donnée à mettre à jour
        query = f"SELECT * FROM {table_nom} WHERE {primary_key_column} = ?"
        try:
            self.cursor.execute(query, (id_a_modifier,))
            resultat = self.cursor.fetchone()
            if resultat:
                # Afficher l'ancienne valeur
                print("\nAncienne valeur :") 
                for colonne_nom, valeur in zip([desc[0] for desc in self.cursor.description], resultat):
                    print(f"{colonne_nom} : {valeur}")

            # Demander la nouvelle valeur à l'utilisateur
            nouvelle_valeur = {}
            for colonne_nom, valeur in zip([desc[0] for desc in self.cursor.description][1:], resultat[1:]):
                nouvelle_valeur[colonne_nom] = input(f"\nEntrez la nouvelle valeur pour {colonne_nom} ({valeur}) : ")

            # Mettre à jour la donnée
            query = f"UPDATE {table_nom} SET "
            params = []
            for colonne_nom, valeur in nouvelle_valeur.items():
                query += f"{colonne_nom} = ?, "
                params.append(valeur)
            query = query.rstrip(', ') + f" WHERE {primary_key_column} = ?"
            params.append(id_a_modifier)
            self.cursor.execute(query, params)
            self.conn.commit()
            print("Mise à jour effectuée avec succès !")
        except sqlite3.Error as e:
            print(f"Erreur lors de la mise à jour : {e}")

    def export_to_csv(self, table_nom, file_nom):
        # Récupérer les colonnes de la table
        colonnes = self.get_columns(table_nom)

        # Ouvrir le fichier CSV en mode écriture
        with open(file_nom +".csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Écrire les en-têtes de colonne
            writer.writerow(colonnes)

            # Récupérer les données de la table
            query = f"SELECT * FROM {table_nom}"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            # Écrire les données dans le fichier CSV
            for row in rows:
                writer.writerow(row)  
        print(f"Exportation réussie vers {file_nom} !")

    def inspect(self):
        class Inspector:
            def __init__(self, db):
                self.db = db

            def get_table_names(self):
                cursor = self.db.cursor
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [row[0] for row in cursor.fetchall()]
                return tables
        return Inspector(self)