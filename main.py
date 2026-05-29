import argparse
import json
import  os
from datetime import date
import csv

print(date.today())
json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
json.dumps([1, 2, 3, {'4': 5, '6': 7}], separators=(',', ':'))

Task_file = 'Task.json'

def charger_tache():
    if not os.path.exists(Task_file):
        return []

    try:
        with open(Task_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Le fichier est vide ou mal formé
        return []

def sauvegarder_tache(task):
    with open(Task_file, 'w', encoding ='utf-8') as f:
        json.dump(task, f, indent=4, ensure_ascii=False)
def ajouter_tache(args):
    task = charger_tache()
    today = date.today()
    new_task = {"id": len(task)+1,
                "titre": args.titre,
                "description": args.description,
                "date": args.date,
                "today": today.isoformat(),
                "statut": False}
    task.append(new_task)
    sauvegarder_tache(task)
    print(f"Votre tâche {args.titre} - {args.description} (Limite: {args.date}) a été ajoutée avec succès")

def supprimer_tache(args):
    task = charger_tache()
    kept_task =[]
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
        print(f"Aucune tâche avec l'ID {args.id} n'a été trouvée.")
        return
    val = removed_task[0]
    title = val['titre']
    describe = val['description']
    date = val['date']
    sauvegarder_tache(kept_task)
    print(' Votre tâche {} - {} (Limite: {}) a été supprimée avec succès'.format(title, describe , date))

def lister(args):
    task = charger_tache()
    if args.terminée:
        print("Voici la liste des tâches terminées:")
        for toto in task:
            val = []
            val.append("ID = {}".format(toto['id']))
            val.append(toto['titre'])
            val.append(toto['description'])
            val.append("Date de création: {}".format(toto["today"]))
            val.append("Date limite: {}".format(toto["date"]))
            if toto['statut']:
                print('[✔]', end=" ")
                print(" - ".join(str(x) for x in val))
    elif args.en_cours:
        print("Voici la liste des tâches terminées:")
        for toto in task:
            val = []
            val.append("ID = {}".format(toto['id']))
            val.append(toto['titre'])
            val.append(toto['description'])
            val.append("Date de création: {}".format(toto["today"]))
            val.append("Date limite: {}".format(toto["date"]))
            if not toto['statut']:
                print('[✗]', end=" ")
                print(" - ".join(str(x) for x in val))
    else:
        print("Voici la liste des tâches:")
        for toto in task:
            val =  []
            val.append("ID = {}".format(toto['id']))
            val.append(toto['titre'])
            val.append(toto['description'])
            val.append("Date de création: {}".format(toto["today"]))
            val.append("Date limite: {}".format(toto["date"]))
            if toto['statut']:
                print('[✔]', end= " ")
                print(" - ".join(str(x) for x in val))
            if not toto['statut']:
                print('[✗]', end=" ")
                print(" - ".join(str(x) for x in val))



def valider_tache(args):
    task = charger_tache()
    for toto in task:
        if not toto['statut']:
            if toto['id'] == args.id:
                toto['statut'] = True
                print(f'Félicitation, vous venez de valider votre tâche: {args.id}!')
        else:
            print(f'La tâche {args.id} a déjà été validé!')
    sauvegarder_tache(task)


def invalider_tache(args):
    task = charger_tache()
    for toto in task:
        if toto['statut']:
            if toto['id'] == args.id:
                toto['statut'] = False
                print(f"Mince, votre tâche {args.id} doit être revalidée")
        else:
            print(f'La tâche {args.id} n\'était déjà pas validé!')
    sauvegarder_tache(task)

def help(args):
    parser.print_help()

def modifier(args):
    task = charger_tache()
    exists = False
    for toto in task:
        if toto['id'] == args.id:
            exists = True
            print(f'La tache {args.id} existe ! \nTraitement en cours')
            if args.titre!= None:
                old_title = toto['titre']
                if old_title == args.titre:
                    print(f'Pas besoin de modifier le titre de la tâche {args.id}')
                else:
                    toto['titre'] = args.titre
                    print(f'Le titre de la tâche {args.id} a été changé de {old_title} à {args.titre} avec succès !')
            if args.description!=None:
                old_description = toto['description']
                if old_description == args.description:
                    print(f'Pas besoin de modifier la description de la tâche {args.id}')
                else:
                    toto['description'] = args.description
                    print(f'La description de la tâche {args.id} a été changé de {old_description} à {args.description} avec succès !')
            if args.date!=None:
                old_date = toto['date']
                if old_date == args.date:
                    print(f'Pas besoin de modifier la date de la tâche {args.id}')
                else:
                    toto['date'] = args.date
                    print(f'La date limite de la tâche {args.id} a été changé de {old_date} à {args.date} avec succès !')
            if args.titre is None and args.description is None and args.date is None:
                print(f'Aucune modification n\'a été apporté a la tache {args.id}')
    if not exists:
        print("Euuuuuuuh, désolé mais la tache n\'existe pas 😅")
    sauvegarder_tache(task)

#Au cas où on souhaite exporter au format csv:

def exporter_csv(args):  # on attend 'args' ici pour rester cohérent avec argparse
    task = charger_tache()
    fields = ["id", "titre", "description", "date", "statut"]  # champs à exporter

    with open("taches.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for t in task:
            writer.writerow({key: t[key] for key in fields})  # filtrer les champs

    print("✅ Export terminé ! Les tâches ont été sauvegardées dans taches.csv")

#création du parser principal
parser = argparse.ArgumentParser(prog="Gestionnaire de tâche", description="gestionnaire des tâches de Luis",
                                 epilog="Maintenant, vous pourrez vous organiser !")

#répertoire des sous commande
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

#Commande bonus :  Export csv
export = subparsers.add_parser(name="exporter", help="Exporter au format csv (bonus)")
export.set_defaults(func=exporter_csv)

#On récupère les arguments de nos parsers
args = parser.parse_args()

if hasattr(args, "func"):
    args.func(args)
else:
    parser.print_help()