import argparse
import os
import json

P = 'Liste_Projet.json'  # Fichier contenant la liste des projets
ACTIVE_PROJECT_FILE = "projet_actif.txt"  # Stocke le projet actif

def NewProject(args):
    # Charger la liste des projets
    if os.path.exists(P):
        try:
            with open(P, "r", encoding="utf-8") as f:
                projets = json.load(f)
        except json.JSONDecodeError:
            projets = []
    else:
        projets = []

    path = args.Project + ".json"

    # Créer le projet s’il n’existe pas
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)

        projets.append(path)
        with open(P, "w", encoding="utf-8") as f:
            json.dump(projets, f, indent=2)

        print(f"✅ Projet '{args.Project}' créé avec succès.")
        return []

    # Charger projet existant
    try:
        with open(path, "r", encoding="utf-8") as f:
            print("ℹ️ Projet déjà existant !")
            return json.load(f)
    except json.JSONDecodeError:
        print("⚠️ Fichier existant vide ou corrompu, retour d'une liste vide.")
        return []

def SelectProject(args):
    projet = args.NomProjet + ".json"

    if os.path.exists(P):
        try:
            with open(P, "r", encoding="utf-8") as f:
                projets = json.load(f)

            if projet in projets:
                with open(ACTIVE_PROJECT_FILE, "w", encoding="utf-8") as f:
                    f.write(projet)
                print(f"✅ Projet sélectionné : {projet}")
            else:
                print(f"❌ Le projet '{args.NomProjet}' n'existe pas dans la liste des projets.")
        except json.JSONDecodeError:
            print("⚠️ Le fichier Liste_Projet.json est vide ou corrompu.")
    else:
        print("⚠️ Aucun projet n'a encore été créé.")


def ListerProject(args):
    if os.path.exists(P):
        try:
            with open(P, "r", encoding="utf-8") as f:
                projects = json.load(f)
            print("📁 Liste des projets existants :")
            for p in projects:
                print("- " + p)
        except json.JSONDecodeError:
            print("⚠️ Erreur : le fichier Liste_Projet.json est vide ou corrompu.")
    else:
        print("ℹ️ Aucun projet enregistré.")

#Récupérer le projet actif
def get_active_project():
    if os.path.exists(ACTIVE_PROJECT_FILE):
        with open(ACTIVE_PROJECT_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    else:
        print("⚠️ Aucun projet actif sélectionné.")
        print("📂 Projets disponibles :")

        if os.path.exists(P):
            try:
                with open(P, "r", encoding="utf-8") as f:
                    projets = json.load(f)
                    for projet in projets:
                        print("- " + projet)
            except json.JSONDecodeError:
                print("❌ Erreur : Liste_Projet.json est vide ou corrompu.")
        else:
            print("❌ Aucun projet trouvé.")

        return None


# ----------------- ARGPARSE -----------------

parser = argparse.ArgumentParser(prog="Gestionnaire")

subparsers = parser.add_subparsers(dest="command")

# NEW
parser_np = subparsers.add_parser(name="New", help="Créer un nouveau projet")
parser_np.add_argument("Project", help="Nom du projet")
parser_np.set_defaults(func=NewProject)

# LIST
parser_listproject = subparsers.add_parser(name="Projet", help="Lister tous les projets")
parser_listproject.set_defaults(func=ListerProject)

# SELECT
parser_select = subparsers.add_parser(name="Select", help="Sélectionner un projet actif")
parser_select.add_argument("NomProjet", help="Nom du projet à activer")
parser_select.set_defaults(func=SelectProject)

# EXECUTION
args = parser.parse_args()

if hasattr(args, "func"):
    args.func(args)
else:
    parser.print_help()

