import pandas as pd
import random

incidents = ["Écran bleu Windows", "Mot de passe oublié", "Panne VPN", "Imprimante bloquée", "Lenteur réseau"]
descriptions = ["Mon PC a crashé", "Je n'arrive plus à me connecter", "Le VPN coupe tout le temps", "impossible d'imprimer le rapport", "Internet rame énormément"]
dates_sales = ["2023-10-12", "12/10/2023", "Oct 12 2023", "2023/10/12 14:30:00", None] 
priorites = ["Haute", "Moyenne", "Basse", "URGENT", "faible", " "]

data = []
for i in range(1, 101): # Génération de 100 tickets
    is_upper = random.random() > 0.8
    desc = random.choice(descriptions)
    
    data.append({
        "ticket_id": f"IT-{i:04d}",
        "category": random.choice(incidents),
        "description": desc.upper() if is_upper else desc,
        "priority": random.choice(priorites),
        "created_at": random.choice(dates_sales)
    })

df = pd.DataFrame(data)
df.to_csv("data/raw_it_tickets.csv", index=False)
print("✅ Fichier data/raw_it_tickets.csv généré avec 100 tickets !")