#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script FACILE pour ajouter des offres de stages manuellement
Pas besoin de scraping - juste remplir les informations !
"""

import json
from datetime import datetime

def charger_donnees():
    """Charge le fichier JSON"""
    try:
        with open('stages_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"derniere_maj": "", "stages": []}

def sauvegarder_donnees(data):
    """Sauvegarde dans le fichier JSON"""
    with open('stages_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def ajouter_stage_interactif():
    """Ajoute un stage en posant des questions"""
    print("\n" + "="*60)
    print("✨ AJOUTER UN NOUVEAU STAGE")
    print("="*60)
    
    # Poser les questions
    company = input("\n1️⃣  Nom de l'entreprise : ")
    title = input("2️⃣  Titre du poste : ")
    
    print("\nDomaines disponibles :")
    print("   - Finance")
    print("   - Analytics")
    print("   - Investment Banking")
    print("   - Risk Management")
    print("   - Wealth Management")
    print("   - Data Science")
    domain = input("3️⃣  Domaine : ")
    
    location = input("4️⃣  Ville : ")
    
    print("\nDurée (exemples: 6 mois, 12 mois, 6-12 mois)")
    duration = input("5️⃣  Durée : ")
    
    print("\nDate de début (exemples: Mars 2026, Août 2026, Variable, Immédiat)")
    startDate = input("6️⃣  Date de début : ")
    
    link = input("7️⃣  Lien vers l'offre : ")
    
    # Créer l'offre
    nouveau_stage = {
        "company": company,
        "title": title,
        "domain": domain,
        "location": location,
        "duration": duration,
        "startDate": startDate,
        "link": link
    }
    
    # Confirmer
    print("\n" + "="*60)
    print("📋 RÉSUMÉ DE L'OFFRE")
    print("="*60)
    for key, value in nouveau_stage.items():
        print(f"   {key:12} : {value}")
    
    confirmer = input("\n✅ Ajouter cette offre ? (oui/non) : ").lower()
    
    if confirmer in ['oui', 'o', 'yes', 'y']:
        # Charger les données
        data = charger_donnees()
        
        # Ajouter le nouveau stage
        data['stages'].append(nouveau_stage)
        
        # Mettre à jour la date
        now = datetime.now()
        data['derniere_maj'] = now.strftime("%d %B %Y - %H:%M")
        
        # Sauvegarder
        sauvegarder_donnees(data)
        
        print("\n🎉 Offre ajoutée avec succès !")
        print(f"📊 Total : {len(data['stages'])} offres dans la base")
        
        # Demander si on veut en ajouter une autre
        continuer = input("\n➕ Ajouter une autre offre ? (oui/non) : ").lower()
        if continuer in ['oui', 'o', 'yes', 'y']:
            ajouter_stage_interactif()
    else:
        print("\n❌ Offre non ajoutée")

def ajouter_stage_rapide(company, title, domain, location, duration, startDate, link):
    """Ajoute un stage rapidement (sans questions)"""
    data = charger_donnees()
    
    nouveau_stage = {
        "company": company,
        "title": title,
        "domain": domain,
        "location": location,
        "duration": duration,
        "startDate": startDate,
        "link": link
    }
    
    data['stages'].append(nouveau_stage)
    
    now = datetime.now()
    data['derniere_maj'] = now.strftime("%d %B %Y - %H:%M")
    
    sauvegarder_donnees(data)
    print(f"✅ {company} - {title} ajouté !")

def voir_statistiques():
    """Affiche les statistiques"""
    data = charger_donnees()
    stages = data.get('stages', [])
    
    print("\n" + "="*60)
    print("📊 STATISTIQUES")
    print("="*60)
    print(f"\nTotal d'offres : {len(stages)}")
    print(f"Dernière mise à jour : {data.get('derniere_maj', 'Jamais')}")
    
    # Par domaine
    domaines = {}
    for stage in stages:
        domain = stage.get('domain', 'Non spécifié')
        domaines[domain] = domaines.get(domain, 0) + 1
    
    print("\n📌 Par domaine :")
    for domain, count in sorted(domaines.items(), key=lambda x: x[1], reverse=True):
        print(f"   • {domain:25} : {count:2} offres")
    
    # Par ville
    villes = {}
    for stage in stages:
        location = stage.get('location', 'Non spécifié')
        villes[location] = villes.get(location, 0) + 1
    
    print("\n📍 Par ville :")
    for ville, count in sorted(villes.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"   • {ville:25} : {count:2} offres")

def menu_principal():
    """Menu principal"""
    while True:
        print("\n" + "="*60)
        print("🎓 GESTIONNAIRE D'OFFRES DE STAGES")
        print("="*60)
        print("\n1️⃣  Ajouter un nouveau stage (mode guidé)")
        print("2️⃣  Voir les statistiques")
        print("3️⃣  Quitter")
        
        choix = input("\n👉 Votre choix : ")
        
        if choix == '1':
            ajouter_stage_interactif()
        elif choix == '2':
            voir_statistiques()
        elif choix == '3':
            print("\n👋 À bientôt !")
            break
        else:
            print("\n❌ Choix invalide, essayez encore")

if __name__ == "__main__":
    print("\n🚀 Bienvenue dans le gestionnaire d'offres de stages !")
    print("Ce script vous aide à ajouter facilement des offres à votre base de données.\n")
    
    menu_principal()
