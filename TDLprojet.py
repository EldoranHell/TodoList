import argparse
import json
import os
from datetime import date, datetime
import csv
from colorama import Fore, Style, init

init(autoreset=True)

print(Fore.LIGHTMAGENTA_EX + str(date.today()))
json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
json.dumps([1, 2, 3, {'4': 5, '6': 7}], separators=(',', ':'))

ACTIVE_PROJECT_FILE = "projet_actif.txt"
P = 'Liste_Projet.json'

def get_active_project():
    if os.path.exists(ACTIVE_PROJECT_FILE):
        with open(ACTIVE_PROJECT_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    else:
        print(Fore.LIGHTMAGENTA_EX + "⚠️ Aucun projet actif sélectionné.")
        print(Fore.CYAN + "📂 Projets disponibles :")

        if os.path.exists(P):
            try:
                with open(P, "r", encoding="utf-8") as f:
                    projets = json.load(f)
                    for projet in projets:
                        print(Fore.LIGHTCYAN_EX + "- " + projet)
            except json.JSONDecodeError:
                print(Fore.RED + "❌ Erreur : Liste_Projet.json est vide ou corrompu.")
        else:
            print(Fore.RED + "❌ Aucun projet trouvé.")

        return None

def charger_tache():
    Task_file = get_active_project()
    if not Task_file or not os.path.exists(Task_file):
        return []

    try:
        with open(Task_file, "r", encoding="utf-8") as f:
            task =  json.load(f)
            for titi in task:
                titi["date"] = datetime.strptime(titi["date"], "%Y-%m-%d").date()
                titi["today"] = datetime.strptime(titi["today"], "%Y-%m-%d").date()
            return task
    except json.JSONDecodeError:
        return []

from datetime import date

def sauvegarder_tache(task):
    Task_file = get_active_project()
    if not Task_file:
        print(Fore.RED + "❌ Impossible de sauvegarder : aucun projet actif.")
        return

    # Conversion des dates en string avant sauvegarde
    for t in task:
        if isinstance(t.get('date'), date):  # Utilisation du type 'date' importé
            t['date'] = t['date'].strftime("%Y-%m-%d")
        if isinstance(t.get('today'), date):  # Utilisation du type 'date' importé
            t['today'] = t['today'].strftime("%Y-%m-%d")

    with open(Task_file, 'w', encoding='utf-8') as f:
        json.dump(task, f, indent=4, ensure_ascii=False)

def ajouter_tache(args):
    task = charger_tache()
    today = date.today()
    date_limite = datetime.strptime(args.date, "%Y-%m-%d").date()
    new_task = {
        "id": len(task)+1,
        "titre": args.titre,
        "description": args.description,
        "date": date_limite.isoformat(),
        "today": today.isoformat(),
        "statut": False
    }
    task.append(new_task)
    sauvegarder_tache(task)
    print(Fore.LIGHTMAGENTA_EX + f"✅ Tâche ajoutée : {args.titre} - {args.description} (Limite: {args.date})")

def supprimer_tache(args):
    task = charger_tache()
    kept_task = []
    removed_task = []
    for toto in task:
        if toto['id'] > args.id:
            toto['id'] -= 1
            kept_task.append(toto)
        elif toto['id'] == args.id:
            removed_task.append(toto)
        else:
            kept_task.append(toto)
    if not removed_task:
        print(Fore.YELLOW + f"⚠️ Aucune tâche avec l'ID {args.id} n'a été trouvée.")
        return
    val = removed_task[0]
    print(Fore.LIGHTMAGENTA_EX + f"🗑️ Tâche supprimée : {val['titre']} - {val['description']} (Limite: {val['date']})")
    sauvegarder_tache(kept_task)

def lister(args):
    task = charger_tache()
    if args.trier:
        task.sort(key=lambda t: t["date"])
        if args.terminée:
            print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "✅ Tâches terminées :")
            for toto in task:
                if toto['statut']:
                    val = [f"ID = {toto['id']}", toto['titre'], toto['description'],
                           f"Créée le : {toto['today']}", f"Limite : {toto['date']}"]
                    print(Fore.GREEN + '[✔] ' + " - ".join(val))
        elif args.en_cours:
            print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "⏳ Tâches en cours :")
            for toto in task:
                if not toto['statut']:
                    val = [f"ID = {toto['id']}", toto['titre'], toto['description'],
                           f"Créée le : {toto['today']}", f"Limite : {toto['date']}"]
                    print(Fore.YELLOW + '[✗] ' + " - ".join(val))
        else:
            print(Fore.LIGHTWHITE_EX + "📋 Toutes les tâches :")
            for toto in task:
                val = [f"ID = {toto['id']}", toto['titre'], toto['description'],
                       f"Créée le : {toto['today']}", f"Limite : {toto['date']}"]
                color = Fore.GREEN if toto['statut'] else Fore.YELLOW
                symbol = '[✔]' if toto['statut'] else '[✗]'
                print(color + symbol + " " + " - ".join(val))
    else:
        if args.terminée:
            print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "✅ Tâches terminées :")
            for toto in task:
                if toto['statut']:
                    val = [f"ID = {toto['id']}", toto['titre'], toto['description'],
                           f"Créée le : {toto['today']}", f"Limite : {toto['date']}"]
                    print(Fore.GREEN + '[✔] ' + " - ".join(val))
        elif args.en_cours:
            print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "⏳ Tâches en cours :")
            for toto in task:
                if not toto['statut']:
                    val = [f"ID = {toto['id']}", toto['titre'], toto['description'],
                           f"Créée le : {toto['today']}", f"Limite : {toto['date']}"]
                    print(Fore.YELLOW + '[✗] ' + " - ".join(val))
        else:
            print(Fore.LIGHTWHITE_EX + "📋 Toutes les tâches :")
            for toto in task:
                val = [f"ID = {toto['id']}", toto['titre'], toto['description'],
                       f"Créée le : {toto['today']}", f"Limite : {toto['date']}"]
                color = Fore.GREEN if toto['statut'] else Fore.YELLOW
                symbol = '[✔]' if toto['statut'] else '[✗]'
                print(color + symbol + " " + " - ".join(val))
def valider_tache(args):
    task = charger_tache()

    find = False
    for toto in task:
        if toto['id'] == args.id:
            find = True
            if not toto['statut']:
                toto['statut'] = True
                print(Fore.LIGHTGREEN_EX + f"🎉 Tâche {args.id} validée !")
            else:
                print(Fore.LIGHTCYAN_EX + f"ℹ️ Tâche {args.id} déjà validée.")
    if not find:
        print(Fore.RED + "❌ Tâche inexistante !")
    sauvegarder_tache(task)

def invalider_tache(args):
    task = charger_tache()
    find = False
    for toto in task:
        if toto['id'] == args.id:
            find = True
            if toto['statut']:
                toto['statut'] = False
                print("🔁 Tâche " + Fore.MAGENTA + Style.BRIGHT + str(args.id) + Style.RESET_ALL + " marquée comme non terminée.")
            else:
                print(Fore.LIGHTCYAN_EX + f"ℹ️ Tâche {args.id} était déjà non validée.")
    if not find:
        print(Fore.RED + "❌ Tâche inexistante !")
    sauvegarder_tache(task)

def help(args):
    parser.print_help()

def modifier(args):
    task = charger_tache()
    exists = False
    for toto in task:
        if toto['id'] == args.id:
            exists = True
            if args.titre and args.titre != toto['titre']:
                print(Fore.LIGHTMAGENTA_EX + f"Titre modifié : {toto['titre']} → {args.titre}")
                toto['titre'] = args.titre
            if args.description and args.description != toto['description']:
                print(Fore.LIGHTMAGENTA_EX + f"Description modifiée : {toto['description']} → {args.description}")
                toto['description'] = args.description
            if args.date and args.date != toto['date']:
                print(Fore.LIGHTMAGENTA_EX + f"Date modifiée : {toto['date']} → {args.date}")
                toto['date'] = args.date
    if not exists:
        print(Fore.RED + "⚠️ Tâche non trouvée.")
    sauvegarder_tache(task)

def exporter_csv(args):
    task = charger_tache()
    fields = ["id", "titre", "description", "date", "statut"]

    with open("taches.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for t in task:
            writer.writerow({key: t[key] for key in fields})

    print(Fore.LIGHTGREEN_EX + "✅ Export terminé !")

def NewProject(args):
    if os.path.exists(P):
        try:
            with open(P, "r", encoding="utf-8") as f:
                projets = json.load(f)
        except json.JSONDecodeError:
            projets = []
    else:
        projets = []

    path = args.Project + ".json"

    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)

        projets.append(path)
        with open(P, "w", encoding="utf-8") as f:
            json.dump(projets, f, indent=2)

        print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT + f"✅ Projet '{args.Project}' créé avec succès.")
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            print(Fore.LIGHTCYAN_EX + "ℹ️ Projet déjà existant.")
            return json.load(f)
    except json.JSONDecodeError:
        print(Fore.RED + "⚠️ Fichier existant vide ou corrompu, retour d'une liste vide.")
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
                print(Fore.CYAN + f"✅ Projet sélectionné : {projet}")
            else:
                print(Fore.RED + f"❌ Le projet '{args.NomProjet}' n'existe pas dans la liste.")
        except json.JSONDecodeError:
            print(Fore.RED + "⚠️ Le fichier Liste_Projet.json est vide ou corrompu.")
    else:
        print(Fore.YELLOW + "⚠️ Aucun projet n'a encore été créé.")

def ListerProject(args):
    if os.path.exists(P):
        try:
            with open(P, "r", encoding="utf-8") as f:
                projects = json.load(f)
            print(Fore.LIGHTMAGENTA_EX + "📁 Liste des projets existants :")
            for p in projects:
                print(Fore.CYAN + "- " + p)
        except json.JSONDecodeError:
            print(Fore.RED + "⚠️ Erreur : le fichier Liste_Projet.json est vide ou corrompu.")
    else:
        print(Fore.YELLOW + "ℹ️ Aucun projet enregistré.")

# Argument parser
parser = argparse.ArgumentParser(prog="Gestionnaire de tâche", description="Gestionnaire des tâches de Luis",
                                 epilog="Maintenant, vous pourrez vous organiser !")
subparsers = parser.add_subparsers(dest="command")

#Commande : help
parser_help = subparsers.add_parser(name="help", help="Comprendre le %(prog)s")
parser_help.set_defaults(func=help)

# Commande : ajouter
parser_ajouter = subparsers.add_parser("ajouter", help="Ajouter une nouvelle tâche")
parser_ajouter.add_argument("titre", type=str, help="Titre de la tâche")
parser_ajouter.add_argument("description", type=str, help="Description de la tâche")
parser_ajouter.add_argument("date", type=str, help="Date limite (YYYY-MM-DD)")
parser_ajouter.set_defaults(func=ajouter_tache)

# Commande : supprimer
parser_supprimer = subparsers.add_parser("supprimer", help="Supprimer une tâche")
parser_supprimer.add_argument("id", type=int, help="ID de la tâche")
parser_supprimer.set_defaults(func=supprimer_tache)

#Commande : lister
parser_lister = subparsers.add_parser(name ="lister", help = "Lister les tâches enregistrées")
parser_lister.add_argument("--terminée", help="affiche uniquement les tâches terminée",
                           action ="store_true")
parser_lister.add_argument("--en_cours", help="affiche uniquement les tâches en cours de complétion",
                           action ="store_true")
parser_lister.add_argument("--trier", help="Trie par date limite",
                           action ="store_true")
parser_lister.set_defaults(func=lister)

#Commande : Valider
parser_valider =  subparsers.add_parser(name ="valider", help="Valider une tâche")
parser_valider.add_argument("id", type = int, help = "ID de la tâche")
parser_valider.set_defaults(func = valider_tache)

#Commande : invalider
parser_invalider =  subparsers.add_parser(name = "invalider", help="Invalider une tâche")
parser_invalider.add_argument("id", type = int, help="Id de la tâche")
parser_invalider.set_defaults(func = invalider_tache)

#Commande : modifier
parser_mod = subparsers.add_parser(name ="modifier", help ="Modifier une tâche déjà écrite")
parser_mod.add_argument('id', type = int, help='id de la tâche a modifier')
parser_mod.add_argument('--titre', type=str, help='Titre a modifier')
parser_mod.add_argument('--description', type = str, help="Description a modifier")
parser_mod.add_argument('--date', type = str, help ='Date a modifier')
parser_mod.set_defaults(func = modifier)

export = subparsers.add_parser("exporter", help="Commande " + Fore.MAGENTA + Style.BRIGHT+ "BONUS" + Style.RESET_ALL+ " permettant d'exporter au format csv")
export.set_defaults(func=exporter_csv)

parser_np = subparsers.add_parser("New", help="Creer un nouveau répertoire pour un nouveau projet")
parser_np.add_argument("Project", type = str)
parser_np.set_defaults(func=NewProject)

parser_listproject = subparsers.add_parser("Projet", help="Lister les projets existant")
parser_listproject.set_defaults(func=ListerProject)

parser_select = subparsers.add_parser("Select", help="Selectionner le projet actif")
parser_select.add_argument("NomProjet", type =str)
parser_select.set_defaults(func=SelectProject)

args = parser.parse_args()

if hasattr(args, "func"):
    args.func(args)
else:
    parser.print_help()
