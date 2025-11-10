import requests
from transformers import AutoTokenizer, AutoModel
import torch
import faiss
import numpy as np
import os
import json
from datetime import datetime

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Steg 1: Hämta bidragsdata från Grants.gov
def fetch_grants_data():
    """
    Hämtar bidrag från Grants.gov API
    Returnerar en lista med bidragsinformation
    """
    print("Hämtar bidrag från Grants.gov...")
    print("OBS: Detta kan ta 1-2 minuter...\n")
    
    # Grants.gov API endpoint (nytt API v1)
    base_url = "https://api.grants.gov/v1/api/search2"
    
    all_grants = []
    
    # Hämta olika kategorier för att få en bra mix
    categories = ["education", "health", "environment", "community", "technology"]
    
    for i, category in enumerate(categories, 1):
        try:
            print(f"[{i}/{len(categories)}] Hämtar kategori: {category}...")
            
            # Använd POST med JSON body enligt nya API:et
            payload = {
                "keyword": category,
                "oppStatuses": "posted",
                "rows": 30  # Färre resultat per kategori för snabbare demo
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            response = requests.post(base_url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                # Nya API:et har strukturen {"data": {"oppHits": [...]}}
                if 'data' in result and 'oppHits' in result['data']:
                    grants = result['data']['oppHits']
                    print(f"  ✅ Hittade {len(grants)} bidrag")
                    
                    for grant in grants:
                        # Skapa en strukturerad representation av bidraget
                        grant_info = {
                            'id': grant.get('id', 'N/A'),
                            'number': grant.get('number', 'N/A'),
                            'title': grant.get('title', 'Ingen titel'),
                            'description': grant.get('synopsis', grant.get('description', 'Ingen beskrivning')),
                            'agency': grant.get('agencyName', 'N/A'),
                            'amount_min': grant.get('awardFloor', 'N/A'),
                            'amount_max': grant.get('awardCeiling', 'N/A'),
                            'deadline': grant.get('closeDate', 'N/A'),
                            'posted_date': grant.get('openDate', 'N/A'),
                            'category': category,
                            'url': f"https://www.grants.gov/search-results-detail/{grant.get('id', '')}"
                        }
                        
                        # Undvik dubbletter
                        if not any(g['id'] == grant_info['id'] for g in all_grants):
                            all_grants.append(grant_info)
                else:
                    print(f"  ⚠️ Ingen 'oppHits' i svaret för {category}")
                    print(f"     Svar: {result.get('msg', 'Inget felmeddelande')}")
            else:
                print(f"  ❌ Fel vid hämtning av {category}: Status {response.status_code}")
                try:
                    error_msg = response.json().get('msg', 'Okänt fel')
                    print(f"     Felmeddelande: {error_msg}")
                except:
                    pass
        
        except requests.exceptions.Timeout:
            print(f"  ⚠️ Timeout för kategorin '{category}' - fortsätter...")
            continue
        except Exception as e:
            print(f"  ⚠️ Fel för kategorin '{category}': {str(e)}")
            continue
    
    print(f"\n✅ Totalt antal unika bidrag hämtade: {len(all_grants)}")
    
    # Om API:et inte fungerade, skapa demo-data
    if len(all_grants) == 0:
        print("\n⚠️ Kunde inte hämta data från Grants.gov API")
        print("Skapar demo-data istället...\n")
        all_grants = create_demo_data()
    
    return all_grants

def create_demo_data():
    """
    Skapar demo-data om API:et inte fungerar
    """
    demo_grants = [
        {
            'id': 'DEMO-001',
            'number': 'ED-2024-001',
            'title': 'Education Excellence Grant for Underserved Youth',
            'description': 'This grant supports educational programs targeting disadvantaged youth in urban and rural communities. Funding can be used for after-school programs, tutoring, mentorship, and educational technology. Priority given to evidence-based interventions.',
            'agency': 'Department of Education',
            'amount_min': '50000',
            'amount_max': '500000',
            'deadline': '2025-03-15',
            'posted_date': '2024-11-01',
            'category': 'Education',
            'url': 'https://www.grants.gov/demo/001'
        },
        {
            'id': 'DEMO-002',
            'number': 'EPA-2024-002',
            'title': 'Environmental Protection and Climate Resilience Initiative',
            'description': 'Support for community-based environmental projects including climate change adaptation, renewable energy, pollution reduction, and ecosystem restoration. Eligible activities include planning, implementation, and monitoring.',
            'agency': 'Environmental Protection Agency',
            'amount_min': '100000',
            'amount_max': '1000000',
            'deadline': '2025-04-30',
            'posted_date': '2024-11-01',
            'category': 'Environment',
            'url': 'https://www.grants.gov/demo/002'
        },
        {
            'id': 'DEMO-003',
            'number': 'HHS-2024-003',
            'title': 'Community Health and Wellness Program',
            'description': 'Funding for community health initiatives including mental health services, substance abuse prevention, chronic disease management, and health education. Priority for underserved populations.',
            'agency': 'Department of Health and Human Services',
            'amount_min': '75000',
            'amount_max': '750000',
            'deadline': '2025-05-15',
            'posted_date': '2024-11-01',
            'category': 'Health',
            'url': 'https://www.grants.gov/demo/003'
        },
        {
            'id': 'DEMO-004',
            'number': 'ED-2024-004',
            'title': 'STEM Education Innovation Fund',
            'description': 'Grants for innovative STEM education programs in K-12 schools. Supports curriculum development, teacher training, equipment purchase, and student engagement activities in science, technology, engineering, and mathematics.',
            'agency': 'Department of Education',
            'amount_min': '25000',
            'amount_max': '300000',
            'deadline': '2025-06-01',
            'posted_date': '2024-11-01',
            'category': 'Education',
            'url': 'https://www.grants.gov/demo/004'
        },
        {
            'id': 'DEMO-005',
            'number': 'HUD-2024-005',
            'title': 'Community Development and Social Services Grant',
            'description': 'Support for community development projects including affordable housing, social services, workforce development, and community infrastructure. Emphasis on projects serving low-income communities.',
            'agency': 'Department of Housing and Urban Development',
            'amount_min': '150000',
            'amount_max': '2000000',
            'deadline': '2025-07-15',
            'posted_date': '2024-11-01',
            'category': 'Community',
            'url': 'https://www.grants.gov/demo/005'
        },
        {
            'id': 'DEMO-006',
            'number': 'HHS-2024-006',
            'title': 'Mental Health Services for Youth',
            'description': 'Funding for mental health programs targeting children and adolescents. Supports counseling services, crisis intervention, prevention programs, and training for mental health professionals.',
            'agency': 'Department of Health and Human Services',
            'amount_min': '100000',
            'amount_max': '800000',
            'deadline': '2025-03-31',
            'posted_date': '2024-11-01',
            'category': 'Health',
            'url': 'https://www.grants.gov/demo/006'
        },
        {
            'id': 'DEMO-007',
            'number': 'EPA-2024-007',
            'title': 'Clean Water Infrastructure Grant',
            'description': 'Support for water quality improvement projects including wastewater treatment, stormwater management, drinking water systems, and water conservation. Technical assistance available.',
            'agency': 'Environmental Protection Agency',
            'amount_min': '200000',
            'amount_max': '5000000',
            'deadline': '2025-08-30',
            'posted_date': '2024-11-01',
            'category': 'Environment',
            'url': 'https://www.grants.gov/demo/007'
        },
        {
            'id': 'DEMO-008',
            'number': 'NSF-2024-008',
            'title': 'Technology Innovation and Workforce Development',
            'description': 'Grants for technology training and workforce development programs. Focus on emerging technologies, digital literacy, coding bootcamps, and career pathways in technology sectors.',
            'agency': 'National Science Foundation',
            'amount_min': '50000',
            'amount_max': '600000',
            'deadline': '2025-04-15',
            'posted_date': '2024-11-01',
            'category': 'Technology',
            'url': 'https://www.grants.gov/demo/008'
        }
    ]
    
    print(f"✅ Skapade {len(demo_grants)} demo-bidrag")
    return demo_grants

# Steg 2: Skapa embedding för bidragsdata
model_name = "sentence-transformers/all-MiniLM-L6-v2"
print("Laddar AI-modell för textanalys...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
print("Modell laddad!")

def create_embeddings(text_list, batch_size=32):
    """
    Skapar embeddings för en lista av texter
    Använder batchar för bättre minneshantering
    """
    all_embeddings = []
    total_batches = (len(text_list) + batch_size - 1) // batch_size
    
    print(f"Skapar embeddings för {len(text_list)} bidrag i {total_batches} batchar...")
    
    for i in range(0, len(text_list), batch_size):
        batch_texts = text_list[i:i+batch_size]
        inputs = tokenizer(batch_texts, padding=True, truncation=True, 
                          max_length=512, return_tensors="pt")
        with torch.no_grad():
            model_output = model(**inputs)
        batch_embeddings = model_output.last_hidden_state.mean(dim=1).numpy()
        all_embeddings.append(batch_embeddings)
        
        if (i // batch_size + 1) % 5 == 0:
            print(f"  Bearbetat batch {i // batch_size + 1}/{total_batches}")
    
    return np.vstack(all_embeddings)

def create_searchable_text(grant):
    """
    Kombinerar relevanta textfält för att skapa sökbar text
    """
    parts = [
        grant['title'],
        grant['description'][:500],  # Begränsa beskrivningslängd
        grant['agency'],
        grant['category']
    ]
    return " ".join([str(p) for p in parts if p and p != 'N/A'])

# Huvudprogram
if __name__ == "__main__":
    print("="*60)
    print("GRANTS.GOV DEMO - INDEXERING")
    print("="*60)
    print()
    
    # Hämta bidragsdata
    grants_data = fetch_grants_data()
    
    if not grants_data:
        print("\n❌ Kunde inte hämta några bidrag. Kontrollera internetanslutningen.")
        exit(1)
    
    print(f"\n✅ Hämtade {len(grants_data)} bidrag")
    
    # Skapa sökbara texter
    print("\nFörbereder texter för indexering...")
    searchable_texts = [create_searchable_text(grant) for grant in grants_data]
    
    # Skapa embeddings
    grant_embeddings = create_embeddings(searchable_texts)
    
    # Skapa data-mappen om den inte finns
    os.makedirs("data", exist_ok=True)
    
    # Steg 3: Lagra embeddings i FAISS för snabb sökning
    print("\nSkapar FAISS-index...")
    dimension = grant_embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(grant_embeddings))
    
    # Spara index
    faiss.write_index(index, "data/grants_index.faiss")
    print(f"  ✅ FAISS-index sparat (dimension: {dimension})")
    
    # Spara bidragsinformation som JSON
    with open("data/grants_data.json", "w", encoding="utf-8") as f:
        json.dump(grants_data, f, indent=2, ensure_ascii=False)
    print(f"  ✅ Bidragsdata sparad")
    
    # Skapa en enkel metadatafil
    with open("data/grants_metadata.txt", "w", encoding="utf-8") as f:
        f.write(f"Indexerad: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Antal bidrag: {len(grants_data)}\n")
        f.write(f"Embedding dimension: {dimension}\n")
    
    print("\n" + "="*60)
    print("✅ INDEXERING KLAR!")
    print("="*60)
    print(f"\nFiler skapade:")
    print(f"  - data/grants_index.faiss")
    print(f"  - data/grants_data.json")
    print(f"  - data/grants_metadata.txt")
    print(f"\nNu kan du köra sökningen med: python demo_grants.py")
    print("="*60)

