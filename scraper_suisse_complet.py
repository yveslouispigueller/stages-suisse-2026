#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scraper pour sites d'emploi SUISSES
Sites : Jobs.ch, Jobup.ch, Travail.swiss, eFinancialCareers.ch
Version adaptée aux débutants
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

def get_headers():
    """Headers pour les requêtes HTTP"""
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    }

def scraper_jobs_ch():
    """
    Scraper pour Jobs.ch
    Un des plus grands sites d'emploi en Suisse
    """
    print("\n🔍 [1/4] Scraping Jobs.ch...")
    print("-" * 70)
    stages = []
    
    try:
        recherches = [
            'finance+internship+zurich',
            'stage+finance+geneva',
            'trainee+finance+basel'
        ]
        
        for terme in recherches:
            print(f"  🔎 Recherche : {terme.replace('+', ' ')}")
            
            url = f"https://www.jobs.ch/en/vacancies/?term={terme}"
            
            try:
                time.sleep(2)
                response = requests.get(url, headers=get_headers(), timeout=15)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Chercher tous les liens d'offres
                    links = soup.find_all('a', href=True)
                    job_links = [link for link in links if '/job/' in link.get('href', '')]
                    
                    for link in job_links[:5]:
                        try:
                            title = link.get_text(strip=True)
                            parent = link.find_parent()
                            
                            # Chercher l'entreprise
                            company = "Entreprise non spécifiée"
                            if parent:
                                company_elem = parent.find('span', class_=lambda x: x and 'company' in str(x).lower())
                                if company_elem:
                                    company = company_elem.get_text(strip=True)
                            
                            if len(title) > 10:
                                stage = {
                                    "company": company,
                                    "title": title,
                                    "domain": "Finance",
                                    "location": "Switzerland",
                                    "duration": "6 mois",
                                    "startDate": "Variable",
                                    "link": f"https://www.jobs.ch{link['href']}" if not link['href'].startswith('http') else link['href']
                                }
                                stages.append(stage)
                        except:
                            continue
                    
                    print(f"  ✓ {len([s for s in stages])} offres trouvées pour cette recherche")
                else:
                    print(f"  ⚠️  Statut HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ Erreur : {str(e)[:60]}")
            
    except Exception as e:
        print(f"  ❌ Erreur générale : {e}")
    
    print(f"  📊 Total Jobs.ch : {len(stages)} offres")
    return stages

def scraper_jobup_ch():
    """
    Scraper pour Jobup.ch
    Plateforme suisse romande et alémanique
    """
    print("\n🔍 [2/4] Scraping Jobup.ch...")
    print("-" * 70)
    stages = []
    
    try:
        recherches = [
            'finance+internship',
            'stage+finance',
            'financial+analyst+trainee'
        ]
        
        for terme in recherches:
            print(f"  🔎 Recherche : {terme.replace('+', ' ')}")
            
            url = f"https://www.jobup.ch/en/jobs/?term={terme}"
            
            try:
                time.sleep(2)
                response = requests.get(url, headers=get_headers(), timeout=15)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Chercher les articles ou divs de jobs
                    job_elements = soup.find_all(['article', 'div'], class_=lambda x: x and 'job' in str(x).lower())
                    
                    for job in job_elements[:5]:
                        try:
                            # Chercher titre
                            title_elem = job.find(['h2', 'h3', 'a'])
                            if not title_elem:
                                continue
                            
                            title = title_elem.get_text(strip=True)
                            
                            # Chercher entreprise
                            company_elem = job.find(['span', 'div', 'p'], class_=lambda x: x and ('company' in str(x).lower() or 'employer' in str(x).lower()))
                            company = company_elem.get_text(strip=True) if company_elem else "Entreprise non spécifiée"
                            
                            # Chercher lien
                            link_elem = job.find('a', href=True)
                            link = link_elem['href'] if link_elem else url
                            if not link.startswith('http'):
                                link = f"https://www.jobup.ch{link}"
                            
                            # Chercher localisation
                            location_elem = job.find(['span', 'div'], class_=lambda x: x and 'location' in str(x).lower())
                            location = location_elem.get_text(strip=True) if location_elem else "Switzerland"
                            
                            if len(title) > 10:
                                stage = {
                                    "company": company,
                                    "title": title,
                                    "domain": "Finance",
                                    "location": location,
                                    "duration": "6 mois",
                                    "startDate": "Variable",
                                    "link": link
                                }
                                stages.append(stage)
                        except:
                            continue
                    
                    print(f"  ✓ {len([s for s in stages])} offres trouvées pour cette recherche")
                else:
                    print(f"  ⚠️  Statut HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ Erreur : {str(e)[:60]}")
            
    except Exception as e:
        print(f"  ❌ Erreur générale : {e}")
    
    print(f"  📊 Total Jobup.ch : {len(stages)} offres")
    return stages

def scraper_travail_swiss():
    """
    Scraper pour Travail.swiss
    Portail officiel du SECO (Secrétariat d'État à l'économie)
    """
    print("\n🔍 [3/4] Scraping Travail.swiss...")
    print("-" * 70)
    stages = []
    
    try:
        # Recherches en français et anglais
        recherches = [
            'finance+internship',
            'stage+finance',
            'stagiaire+finance'
        ]
        
        for terme in recherches:
            print(f"  🔎 Recherche : {terme.replace('+', ' ')}")
            
            # URL du portail officiel
            url = f"https://www.travail.swiss/job-search/?keywords={terme}"
            
            try:
                time.sleep(2)
                response = requests.get(url, headers=get_headers(), timeout=15)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Structure du site officiel
                    job_listings = soup.find_all(['article', 'li', 'div'], class_=lambda x: x and ('job' in str(x).lower() or 'listing' in str(x).lower()))
                    
                    for job in job_listings[:5]:
                        try:
                            # Titre
                            title_elem = job.find(['h2', 'h3', 'h4', 'a', 'strong'])
                            if not title_elem:
                                continue
                            
                            title = title_elem.get_text(strip=True)
                            
                            # Entreprise
                            company_elem = job.find(['span', 'div', 'p'], text=lambda t: t and ('SA' in str(t) or 'AG' in str(t) or 'GmbH' in str(t) or 'Ltd' in str(t)))
                            if not company_elem:
                                company_elem = job.find(['span', 'div'], class_=lambda x: x and 'company' in str(x).lower())
                            company = company_elem.get_text(strip=True) if company_elem else "Entreprise non spécifiée"
                            
                            # Lien
                            link_elem = job.find('a', href=True)
                            link = link_elem['href'] if link_elem else url
                            if not link.startswith('http'):
                                link = f"https://www.travail.swiss{link}"
                            
                            # Location
                            location = "Switzerland"
                            for text in job.stripped_strings:
                                if any(city in text for city in ['Zurich', 'Geneva', 'Genève', 'Lausanne', 'Basel', 'Bern', 'Berne']):
                                    location = text.strip()
                                    break
                            
                            if len(title) > 10:
                                stage = {
                                    "company": company,
                                    "title": title,
                                    "domain": "Finance",
                                    "location": location,
                                    "duration": "6 mois",
                                    "startDate": "Variable",
                                    "link": link
                                }
                                stages.append(stage)
                        except:
                            continue
                    
                    print(f"  ✓ {len([s for s in stages])} offres trouvées pour cette recherche")
                else:
                    print(f"  ⚠️  Statut HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ Erreur : {str(e)[:60]}")
            
    except Exception as e:
        print(f"  ❌ Erreur générale : {e}")
    
    print(f"  📊 Total Travail.swiss : {len(stages)} offres")
    return stages

def scraper_efinancialcareers():
    """
    Scraper pour eFinancialCareers.ch
    Site spécialisé dans les emplois finance
    """
    print("\n🔍 [4/4] Scraping eFinancialCareers.ch...")
    print("-" * 70)
    stages = []
    
    try:
        recherches = [
            'internship',
            'trainee',
            'graduate'
        ]
        
        for terme in recherches:
            print(f"  🔎 Recherche : {terme}")
            
            # URL spécialisée finance
            url = f"https://www.efinancialcareers.ch/jobs/search?keywords={terme}&location=Switzerland"
            
            try:
                time.sleep(2)
                response = requests.get(url, headers=get_headers(), timeout=15)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Structure eFinancialCareers
                    job_cards = soup.find_all(['article', 'div', 'li'], class_=lambda x: x and ('job' in str(x).lower() or 'result' in str(x).lower()))
                    
                    for card in job_cards[:5]:
                        try:
                            # Titre
                            title_elem = card.find(['h2', 'h3', 'a'], class_=lambda x: x and 'title' in str(x).lower())
                            if not title_elem:
                                title_elem = card.find(['h2', 'h3', 'a'])
                            
                            if not title_elem:
                                continue
                            
                            title = title_elem.get_text(strip=True)
                            
                            # Entreprise
                            company_elem = card.find(['span', 'div', 'p'], class_=lambda x: x and ('company' in str(x).lower() or 'employer' in str(x).lower()))
                            if not company_elem:
                                company_elem = card.find(['span', 'div'], text=lambda t: t and any(word in str(t) for word in ['Bank', 'Group', 'AG', 'SA']))
                            company = company_elem.get_text(strip=True) if company_elem else "Entreprise non spécifiée"
                            
                            # Lien
                            link_elem = card.find('a', href=True)
                            link = link_elem['href'] if link_elem else url
                            if not link.startswith('http'):
                                link = f"https://www.efinancialcareers.ch{link}"
                            
                            # Location
                            location_elem = card.find(['span', 'div'], class_=lambda x: x and 'location' in str(x).lower())
                            location = location_elem.get_text(strip=True) if location_elem else "Switzerland"
                            
                            # Filtrer pour garder seulement les stages/internships
                            if len(title) > 10 and any(word in title.lower() for word in ['intern', 'stage', 'trainee', 'graduate']):
                                stage = {
                                    "company": company,
                                    "title": title,
                                    "domain": "Finance",
                                    "location": location,
                                    "duration": "6 mois",
                                    "startDate": "Variable",
                                    "link": link
                                }
                                stages.append(stage)
                        except:
                            continue
                    
                    print(f"  ✓ {len([s for s in stages])} offres trouvées pour cette recherche")
                else:
                    print(f"  ⚠️  Statut HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ Erreur : {str(e)[:60]}")
            
    except Exception as e:
        print(f"  ❌ Erreur générale : {e}")
    
    print(f"  📊 Total eFinancialCareers : {len(stages)} offres")
    return stages

def nettoyer_doublons(stages):
    """Supprime les doublons basés sur entreprise + titre"""
    vus = set()
    uniques = []
    
    for stage in stages:
        # Clé unique
        cle = (
            stage['company'].lower().strip(),
            stage['title'].lower().strip()
        )
        
        if cle not in vus and len(stage['title']) > 10:
            vus.add(cle)
            uniques.append(stage)
    
    return uniques

def fusionner_avec_existants(nouveaux, anciens):
    """Fusionne les nouvelles offres avec les anciennes"""
    nouveaux_dict = {}
    
    for stage in nouveaux:
        cle = (stage['company'].lower().strip(), stage['title'].lower().strip())
        nouveaux_dict[cle] = stage
    
    for ancien in anciens:
        cle = (ancien['company'].lower().strip(), ancien['title'].lower().strip())
        if cle not in nouveaux_dict:
            nouveaux_dict[cle] = ancien
    
    return list(nouveaux_dict.values())

def main():
    """Fonction principale"""
    print("="*70)
    print("🇨🇭 SCRAPER SITES D'EMPLOI SUISSES - VERSION COMPLÈTE")
    print("="*70)
    print("\n📍 Sites ciblés :")
    print("   1. Jobs.ch")
    print("   2. Jobup.ch")
    print("   3. Travail.swiss (portail officiel SECO)")
    print("   4. eFinancialCareers.ch")
    
    print("\n⚠️  IMPORTANT :")
    print("   • Le scraping peut échouer si les sites bloquent les robots")
    print("   • Les structures HTML changent régulièrement")
    print("   • Résultats variables selon les sites")
    print("   • Pour de meilleurs résultats : combinez avec l'ajout manuel\n")
    
    # Charger données
    data = charger_donnees()
    anciens_stages = data.get('stages', [])
    
    print(f"📊 Base actuelle : {len(anciens_stages)} offres\n")
    
    input("Appuyez sur ENTRÉE pour démarrer le scraping... ")
    
    print("\n" + "="*70)
    print("🚀 DÉBUT DU SCRAPING")
    print("="*70)
    
    # Collecter toutes les offres
    tous_nouveaux = []
    
    # 1. Jobs.ch
    tous_nouveaux.extend(scraper_jobs_ch())
    
    # 2. Jobup.ch
    tous_nouveaux.extend(scraper_jobup_ch())
    
    # 3. Travail.swiss
    tous_nouveaux.extend(scraper_travail_swiss())
    
    # 4. eFinancialCareers
    tous_nouveaux.extend(scraper_efinancialcareers())
    
    print("\n" + "="*70)
    print("🧹 NETTOYAGE DES DOUBLONS")
    print("="*70)
    
    # Nettoyer doublons
    avant_nettoyage = len(tous_nouveaux)
    tous_nouveaux = nettoyer_doublons(tous_nouveaux)
    print(f"  Avant : {avant_nettoyage} offres")
    print(f"  Après : {len(tous_nouveaux)} offres")
    print(f"  Doublons supprimés : {avant_nettoyage - len(tous_nouveaux)}")
    
    # Résultats
    print("\n" + "="*70)
    print("📊 RÉSULTATS DU SCRAPING")
    print("="*70)
    
    if tous_nouveaux:
        print(f"\n✨ {len(tous_nouveaux)} nouvelles offres trouvées !\n")
        
        # Aperçu
        print("📋 Aperçu des offres :")
        for i, stage in enumerate(tous_nouveaux[:10], 1):
            print(f"\n   {i}. {stage['title'][:65]}")
            print(f"      🏢 {stage['company']}")
            print(f"      📍 {stage['location']}")
        
        if len(tous_nouveaux) > 10:
            print(f"\n   ... et {len(tous_nouveaux) - 10} autres offres")
        
        # Fusionner
        tous_stages = fusionner_avec_existants(tous_nouveaux, anciens_stages)
        
        print(f"\n📈 Statistiques :")
        print(f"   • Nouvelles offres : {len(tous_nouveaux)}")
        print(f"   • Anciennes offres : {len(anciens_stages)}")
        print(f"   • Total final : {len(tous_stages)}")
        print(f"   • Gain : +{len(tous_stages) - len(anciens_stages)} offres")
        
        # Sauvegarder
        now = datetime.now()
        data['derniere_maj'] = now.strftime("%d %B %Y - %H:%M")
        data['stages'] = tous_stages
        
        sauvegarder_donnees(data)
        
        print("\n✅ Fichier stages_data.json mis à jour !")
        
        # Stats par domaine
        print("\n" + "="*70)
        print("📊 STATISTIQUES PAR DOMAINE")
        print("="*70)
        
        domaines = {}
        for stage in tous_stages:
            domain = stage.get('domain', 'Non spécifié')
            domaines[domain] = domaines.get(domain, 0) + 1
        
        for domain, count in sorted(domaines.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {domain:25} : {count} offres")
        
    else:
        print("\n⚠️  Aucune nouvelle offre trouvée")
        print("\n💡 Raisons possibles :")
        print("   • Les sites bloquent les robots")
        print("   • Aucune offre disponible actuellement")
        print("   • Structure HTML des sites changée")
        print("\n📝 Solution : Utilisez l'outil d'ajout manuel")
    
    print("\n" + "="*70)
    print("🎉 SCRAPING TERMINÉ !")
    print("="*70)
    
    print("\n📌 Prochaines étapes :")
    print("   1. Vérifiez stages_data.json")
    print("   2. Uploadez sur GitHub")
    print("   3. Votre site sera mis à jour automatiquement")
    print("\n💡 Conseil : Lancez ce script 1-2 fois par semaine maximum\n")

if __name__ == "__main__":
    main()
