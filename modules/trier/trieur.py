from pathlib import Path
import shutil
import yaml


def formatage_path(path: Path) -> Path:
    return path.expanduser().resolve()


def est_autorise(dossier: Path, dossiers_autorises: list[Path]) -> bool:
    chemin_absolu = formatage_path(dossier)

    if dossier_existe(chemin_absolu) and chemin_absolu.is_dir():
        for chemin_autorise in dossiers_autorises:
            if chemin_absolu == formatage_path(chemin_autorise):
                return True
        return False

    chemin_parent = chemin_absolu.parent
    for chemin_autorise in dossiers_autorises:
        chemin_autorise_formate = formatage_path(chemin_autorise)
        if chemin_parent.is_relative_to(chemin_autorise_formate):
            return True
    return False


def charger_config(chemin_config: Path) -> list[Path]:
    with open(chemin_config, "r", encoding="utf-8") as fichier:
        contenu = yaml.safe_load(fichier)
        dossiers_autorises = []

        for element in contenu["dossiers_autorises"]:
            chemin_formate = formatage_path(Path(element["chemin"]))
            dossiers_autorises.append(chemin_formate)

    return dossiers_autorises


def dossier_existe(dossier: Path) -> bool:
    return formatage_path(dossier).exists()


def creer_dossier(dossier: Path) -> bool:
    try:
        if dossier_existe(dossier):
            print("Le dossier existe déjà.")
            return False

        formatage_path(dossier).mkdir(parents=True, exist_ok=True)
        print(f"Le dossier a été créé : {dossier}")
        return True
    except PermissionError as erreur:
        print(f"Erreur de permission : {erreur}")
        return False


def deplacer(fichier: Path, dossier_cible: Path, dossiers_autorises: list[Path]) -> bool:
    try:
        if not dossier_existe(fichier):
            print("Le fichier n'existe pas.")
            return False
        if not est_autorise(fichier, dossiers_autorises):
            print(f"Vous n'êtes pas autorisé à deplacér le fichier {fichier}")
            return False

        if dossier_existe(dossier_cible):
            if not est_autorise(dossier_cible, dossiers_autorises):
                print(f"Vous n'êtes pas autorisé à modifier le dossier cible : {dossier_cible}")
                return False
        else:
            if not est_autorise(dossier_cible.parent, dossiers_autorises):
                print(f"Vous n'êtes pas autorisé à modifier le dossier parent : {dossier_cible.parent}")
                return False

            creer_dossier(dossier_cible)
            print(f"Dossier cible après création : {dossier_cible}")
        destination = formatage_path(dossier_cible) / fichier.name
        shutil.move(formatage_path(fichier), destination)
        print(f"Fichier {fichier} déplacé vers : {destination}")
        return True
    except PermissionError as erreur:
        print(f"Erreur de permission : {erreur}")
        return False


if __name__ == "__main__":
    config = charger_config(Path("config.yaml"))
    print(config)
    dossiers = charger_config(Path("config.yaml"))

    # # Cas 1 — dossier existant dans la liste
    # test1 = Path("~/Desktop/test_organisation")
    # print(est_autorise(test1, dossiers))  # True

    # # Cas 2 — dossier existant pas dans la liste
    # test2 = Path("~/Desktop")
    # print(est_autorise(test2, dossiers))  # False

    # # Cas 3 — dossier inexistant, parent autorisé
    # test3 = Path("~/Desktop/test_organisation/PDF")
    # print(est_autorise(test3, dossiers))  # True

    # # Cas 4 — fichier existant dans dossier autorisé
    # test4 = Path("~/Desktop/test_organisation/test.pdf")
    # print(est_autorise(test4, dossiers))  # True

    # # Cas 5 — fichier existant hors dossier autorisé
    # test5 = Path("~/Documents/secret.pdf")
    # print(est_autorise(test5, dossiers))  # False

    # Cas 1 — déplacement valide dossier inexistant
    # deplacer(
    #     Path("~/Desktop/test_organisation/test.pdf"),
    #     Path("~/Desktop/test_organisation/PDF"),
    #     dossiers
    # )

    # Cas 2 — fichier source non autorisé fichier se trouve dans un dossier non autoriser
    # deplacer(
    #     Path("~/Documents/secret.pdf"),
    #     Path("~/Desktop/test_organisation/PDF"),
    #     dossiers
    # )

    # Cas 3 — dossier cible non autorisé
    # deplacer(
    #     Path("~/Desktop/test_organisation/test1.txt"),
    #     Path("~/Downloads/PDF"),
    #     dossiers
    # )