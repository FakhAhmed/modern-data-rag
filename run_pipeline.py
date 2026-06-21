import subprocess
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_task(command, cwd):
    print(f"🚀 Lancement de : {command} dans {cwd}")
    result = subprocess.run(command, shell=True, cwd=cwd)
    if result.returncode != 0:
        print(f"❌ Erreur sur la tâche : {command}")
        exit(1)

# 1. dbt run (avec le bon dossier de profil)
run_task("dbt run --profiles-dir .", cwd=f"{BASE_DIR}/dbt_transform")

# 2. Vectorisation
run_task("python scripts/build_vector_db.py", cwd=BASE_DIR)

print("✅ Pipeline terminé avec succès !")