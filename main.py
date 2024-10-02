from database import *

def menu():

    BDD = None
    while True:
        print("\n" + "*" * 40)
        print("*" + " " * 38 + "*")
        print("*  Menu  *" + " " * 34 + "*")
        print("*" + " " * 38 + "*")
        print("* 1. Créer la base de données" + " " * 18+ "*")
        print("* 2. Créer une table" + " " * 29 + "*")
        print("* 3. Insérer une donnée" + " " * 26 + "*")
        print("* 4. Lister les données" + " " * 25 + "*")
        print("* 5. Mettre à jour" + " " * 28 + "*")
        print("* 6. Supprimer" + " " * 32 + "*")
        print("* 7. Rechercher" + " " * 31 + "*")   
        print("* 8. Exporter une base de donnée" + " " * 15 + "*")
        print("* 0. Quitter" + " " * 32 + "*")
        print("*" + " " * 38 + "*")
        print("*" * 40)

        choice = input("Choisir une option: ")

        if choice == '1':
            db_nom= input('entrer le nom de la base de donnée: ')
            BDD = DatabaseManager(db_nom)
            print(f"Création de la base de données {db_nom}...")

        elif choice == '2':
            db_nom = input('entrer le nom de la base oû créer la table: ')
            BDD = DatabaseManager(db_nom)
            table_nom = input('entrer le nom de la table à créer: ')
            nb_colonnes = int(input("Entrez le nombre de colonnes : "))
            colonnes = {}

            for i in range(nb_colonnes):
                if i == 0:
                    colonne_nom = input("Entrez le nom de la clé primaire : ")
                    colonne_type = "entier"
                    if colonne_type.lower() == "entier":
                        colonne_type = "INTEGER"

                    elif colonne_type.lower() == "caractere":
                        colonne_type = "TEXT"

                    colonnes[colonne_nom] = colonne_type
                else:
                    colonne_nom = input(f"Entrez le nom de la colonne {i} : ")
                    colonne_type = input(f"Entrez le type de la colonne {i} (caractère ou entier) : ")

                # Convertir le type de colonne en type SQL
                if colonne_type.lower() == "entier":
                    colonne_type = "INTEGER"
                elif colonne_type.lower() == "caractere":
                    colonne_type = "TEXT"

                colonnes[colonne_nom] = colonne_type

                # Appeler la méthode create_table avec les colonnes définies
            BDD.create_table(table_nom, colonnes) 

        elif choice == '3':
            db_nom = input('entrer le nom de la base de donnée : ')
            BDD = DatabaseManager(db_nom)
            table_nom = input('entrer le nom de la table : ')

            # Récupérer les colonnes de la table
            colonnes = BDD.get_columns(table_nom)

            # Demander les valeurs à insérer
            valeurs = {}
            for colonne in colonnes:
                if colonne == colonnes[0]:  # Ignorer la clé primaire
                    continue
                valeur = input(f"Entrez la valeur pour la colonne {colonne} : ")
                valeurs[colonne] = valeur

            # Insérer les données dans la table
            BDD.insert_data(table_nom, valeurs)
        elif choice == '4':
            db_nom = input('entrer le nom de la base de donnée : ')
            BDD = DatabaseManager(db_nom)
            BDD.read()

        elif choice == "5":
            db_nom = input('entrer le nom de la base de donnée : ')
            db_manager = DatabaseManager(db_nom)
            table_nom = input('entrer le nom de la table: ')
            db_manager.update(table_nom)

        elif choice == '6':
            db_nom = input('entrer le nom de la base de donnée : ')
            BDD = DatabaseManager(db_nom)

            # Afficher les lignes de la table
            print("Lignes de la table :")
            BDD.read()

            # Demander à l'utilisateur de sélectionner l'ID de la ligne à supprimer
            id = int(input("\nEntrer l'ID de la ligne à supprimer : "))

            # Supprimer la ligne sélectionnée
            BDD.delete(table_nom, id)

            print("element supprimer avec succes")
        elif choice == '7':
            db_nom = input('entrer le nom de la base de donnée : ')
            BDD = DatabaseManager(db_nom)
            table_nom = input('entrer le nom de la table à rechercher : ')
            colonne_nom = input('entrer le nom de la colonne à rechercher : ')
            valeur = input('entrer la valeur à rechercher : ')

            # Rechercher les lignes correspondantes
            lignes = BDD.search(table_nom, colonne_nom, valeur)

            # Afficher les résultats de la recherche
            print("\nRésultats de la recherche :")
            for ligne in lignes:
                print(ligne)

        elif choice == '8':
            db_nom = input('Entrer le nom de la base de données : ')
            BDD = DatabaseManager(db_nom)

            # Get the Inspector object
            inspector = BDD.inspect()

            # Get a list of all tables in the database
            tables = inspector.get_table_names()

            # Export each table to a separate CSV file
            for table_nom in tables:
                file_nom = f"{db_nom}_{table_nom}"
                BDD.export_to_csv(table_nom, file_nom)
        elif choice == '0':
                print("Programme terminé...\n")
                break
        else:
            print("Invalid option")

    # if __name__ == "__main__":
    #     main()

menu()
