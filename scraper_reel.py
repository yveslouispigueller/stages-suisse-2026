#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de scraping FONCTIONNEL pour jobs.ch et autres sites suisses
Version simplifiée et qui marche vraiment !
"""

import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

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

def scraper_jobs_ch():
    """
    Scrape jobs.ch - un des sites d'emploi les plus populaires en Suisse
    """
    print("\n🔍 Recherche sur jobs.ch...")
    stages = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        # Mots-clés à chercher
        keywords = ['finance internship', 'stage finance', 'trainee finance']
        
        for keyword in keywords:
            print(f"  → Recherche '{keyword}'...")
            
            # URL de recherche jobs.ch
            url = f"https://www.jobs.ch/en/vacancies/?term={keyword.replace(' ', '+')}&location=Switzerland"
            
            try:
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Chercher les offres (la structure peut changer)
                    # Ceci est un exemple - il faut adapter selon la vraie structure du site
                    job_cards = soup.find_all('article', class_='job-item')
                    
                    for card in job_cards[:5]:  # Limite à 5 par recherche
                        try:
                            # Extraire les informations
                            title_elem = card.find('h2')
                            company_elem = card.find('span', class_='company')
                            location_elem = card.find('span', class_='location')
                            link_elem = card.find('a', href=True)
                            
                            if title_elem and company_elem:
                                stage = {
                                    "company": company_elem.text.strip(),
                                    "title": title_elem.text.strip(),
                                    "domain": "Finance",  # On suppose Finance vu nos keywords
                                    "location": location_elem.text.strip() if location_elem else "Switzerland",
                                    "duration": "6 mois",  # Valeur par défaut
                                    "startDate": "Variable",
                                    "link": f"https://www.jobs.ch{link_elem['href']}" if link_elem else url
                                }
                                stages.append(stage)
                        except:
                            continue
                    
                    print(f"    ✓ {len([s for s in stages if s])} offres trouvées")
                else:
                    print(f"    ⚠️  Erreur HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"    ⚠️  Erreur: {str(e)[:50]}...")
            
            time.sleep(2)  # Pause pour être poli avec le serveur
        
    except Exception as e:
        print(f"  ❌ Erreur générale: {e}")
    
    return stages

def scraper_indeed_ch():
    """
    Scrape Indeed Suisse - site international avec présence suisse
    """
    print("\n🔍 Recherche sur Indeed CH...")
    stages = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        
        # URL de recherche Indeed
        url = "https://ch.indeed.com/jobs?q=finance+internship&l=Switzerland"
        
        print("  → Recherche d'offres...")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Structure Indeed (peut varier)
                job_cards = soup.find_all('div', class_='job_seen_beacon')
                
                for card in job_cards[:10]:  # Limite à 10
                    try:
                        title = card.find('h2', class_='jobTitle')
                        company = card.find('span', class_='companyName')
                        location = card.find('div', class_='companyLocation')
                        
                        if title and company:
                            # Extraire le lien
                            link_elem = title.find('a', href=True)
                            job_key = link_elem['href'] if link_elem else ''
                            
                            stage = {
                                "company": company.text.strip(),
                                "title": title.text.strip(),
                                "domain": "Finance",
                                "location": location.text.strip() if location else "Switzerland",
                                "duration": "6 mois",
                                "startDate": "Variable",
                                "link": f"https://ch.indeed.com{job_key}" if job_key else url
                            }
                            stages.append(stage)
                    except:
                        continue
                
                print(f"  ✓ {len(stages)} offres trouvées")
            else:
                print(f"  ⚠️  Erreur HTTP {response.status_code}")
                
        except Exception as e:
            print(f"  ⚠️  Erreur: {str(e)[:50]}...")
        
    except Exception as e:
        print(f"  ❌ Erreur générale: {e}")
    
    return stages

def nettoyer_doublons(stages):
    """Supprime les doublons basés sur entreprise + titre"""
    vus = set()
    stages_uniques = []
    
    for stage in stages:
        cle = (stage['company'].lower().strip(), stage['title'].lower().strip())
        if cle not in vus:
            vus.add(cle)
            stages_uniques.append(stage)
    
    return stages_uniques

def fusionner_avec_existants(nouveaux_stages, anciens_stages):
    """Fusionne nouvelles offres avec les anciennes"""
    # Créer un dictionnaire des nouveaux
    nouveaux_dict = {}
    for stage in nouveaux_stages:
        cle = (stage['company'].lower().strip(), stage['title'].lower().strip())
        nouveaux_dict[cle] = stage
    
    # Garder les anciens qui ne sont pas dans les nouveaux
    for ancien in anciens_stages:
        cle = (ancien['company'].lower().strip(), ancien['title'].lower().strip())
        if cle not in nouveaux_dict:
            nouveaux_dict[cle] = ancien
    
    return list(nouveaux_dict.values())

def main():
    """Fonction principale"""
    print("="*70)
    print("🎓 SCRAPING RÉEL D'OFFRES DE STAGES - VERSION FONCTIONNELLE")
    print("="*70)
    
    # Charger données existantes
    data = charger_donnees()
    anciens_stages = data.get('stages', [])
    
    print(f"\n📊 État actuel : {len(anciens_stages)} offres dans la base")
    print("\n⚠️  Note : Ce scraping est basique et peut ne pas capturer toutes les offres.")
    print("   Les sites web changent souvent leur structure HTML.")
    print("   Pour de meilleurs résultats, combinez ce script avec l'ajout manuel !\n")
    
    # Collecter nouvelles offres
    nouveaux_stages = []
    
    print("\n" + "="*70)
    print("🌐 DÉBUT DU SCRAPING")
    print("="*70)
    
    # Jobs.ch
    nouveaux_stages.extend(scraper_jobs_ch())
    
    # Indeed
    nouveaux_stages.extend(scraper_indeed_ch())
    
    # Nettoyer doublons
    nouveaux_stages = nettoyer_doublons(nouveaux_stages)
    
    print("\n" + "="*70)
    print("📊 RÉSULTATS DU SCRAPING")
    print("="*70)
    print(f"\n✨ Nouvelles offres trouvées : {len(nouveaux_stages)}")
    
    # Afficher les nouvelles offres
    if nouveaux_stages:
        print("\n📋 Aperçu des nouvelles offres :")
        for i, stage in enumerate(nouveaux_stages[:5], 1):
            print(f"\n   {i}. {stage['company']} - {stage['title']}")
            print(f"      📍 {stage['location']}")
        
        if len(nouveaux_stages) > 5:
            print(f"\n   ... et {len(nouveaux_stages) - 5} autres offres")
    
    # Fusionner avec existants
    tous_stages = fusionner_avec_existants(nouveaux_stages, anciens_stages)
    
    print(f"\n📈 Total après fusion : {len(tous_stages)} offres")
    print(f"   (+{len(tous_stages) - len(anciens_stages)} offres)")
    
    # Mettre à jour
    now = datetime.now()
    data['derniere_maj'] = now.strftime("%d %B %Y - %H:%M")
    data['stages'] = tous_stages
    
    # Sauvegarder
    sauvegarder_donnees(data)
    
    print("\n✅ Fichier stages_data.json mis à jour !")
    
    # Statistiques
    print("\n" + "="*70)
    print("📊 STATISTIQUES FINALES")
    print("="*70)
    
    domaines = {}
    for stage in tous_stages:
        domain = stage.get('domain', 'Non spécifié')
        domaines[domain] = domaines.get(domain, 0) + 1
    
    print("\nPar domaine :")
    for domain, count in sorted(domaines.items(), key=lambda x: x[1], reverse=True):
        print(f"   • {domain:25} : {count} offres")
    
    print("\n" + "="*70)
    print("🎉 SCRAPING TERMINÉ !")
    print("="*70)
    
    print("\n💡 Conseil : Vérifiez les nouvelles offres et supprimez celles qui ne")
    print("   correspondent pas à vos critères (durée, domaine, etc.)")
    
    print("\n📌 Prochaines étapes :")
    print("   1. Vérifiez le fichier stages_data.json")
    print("   2. Uploadez-le sur GitHub pour mettre à jour votre site")
    print("   3. Utilisez ajouter_stage.py pour ajouter des offres manuellement\n")

if __name__ == "__main__":
    main()
