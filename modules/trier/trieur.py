from pathlib import Path
import yaml
def dossier_autorise(dossier: Path, dossiers_autorises: list[Path]) -> bool:
    path_absolut = dossier.expanduser().resolve() #corriger la forme du path pour pouvoir utiliser is_relativa_to
    autorise = False
    i = len(dossiers_autorises)-1
    while not autorise and i >= 0:
        path = dossiers_autorises[i].expanduser().resolve()
        if path_absolut.is_relative_to(path):
            autorise = True
        i-=1
    return autorise


def charger_config(chemin_config: Path) -> list[Path]:
    with open(chemin_config, "r") as f:
        contenu = yaml.safe_load(f)
        dossier_autorises = []
        
        for elemnt in contenu["dossiers_autorises"]:
            path_formate = Path(elemnt["chemin"]).expanduser().resolve()
            dossier_autorises.append(path_formate)
    return dossier_autorises

def dossier_existe(dossier: Path) -> bool :
    return dossier.exists()

def creer_dossier(dossier: Path) -> bool : 
    creer = False
    try:
        if dossier_existe(dossier): 
            print("Dossier existe déjà")
        else:
            dossier.mkdir(parents=True, exist_ok=True)
            creer = True
    except PermissionError as e:
        print(f"Erreur de permission : {e}")
    return creer

    

#testes
if __name__ == "__main__":
    config = charger_config(Path("config.yaml"))
    print(config)
    dossiers = charger_config(Path("config.yaml"))
    
    test1 = Path("~/Desktop/test_organisation/monfichier.pdf")
    print(dossier_autorise(test1, dossiers))  # doit afficher True
    test2 = Path("~/Documents/secret.pdf")
    print(dossier_autorise(test2, dossiers))  # doit afficher False