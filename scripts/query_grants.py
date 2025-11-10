import faiss
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch
import os
import json
from datetime import datetime

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Ladda FAISS-index och bidragsdata
print("Laddar index och data...")
try:
    index = faiss.read_index("data/grants_index.faiss")
    print(f"  ✅ FAISS-index laddat ({index.ntotal} bidrag)")
except:
    print("  ❌ Kunde inte ladda FAISS-index. Kör först: python scripts/fetch_and_index_grants.py")
    exit(1)

try:
    with open("data/grants_data.json", "r", encoding="utf-8") as f:
        grants_data = json.load(f)
    print(f"  ✅ Bidragsdata laddad ({len(grants_data)} bidrag)")
except:
    print("  ❌ Kunde inte ladda bidragsdata.")
    exit(1)

# Ladda AI-modell
print("Laddar AI-modell...")
model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
print("  ✅ Modell laddad!\n")

def create_query_embedding(query):
    """
    Skapar embedding för en användarfråga
    """
    inputs = tokenizer([query], padding=True, truncation=True, 
                      max_length=512, return_tensors="pt")
    with torch.no_grad():
        model_output = model(**inputs)
    query_embedding = model_output.last_hidden_state.mean(dim=1).numpy()
    return query_embedding

def format_amount(amount_min, amount_max):
    """
    Formaterar bidragsbelopp på ett läsbart sätt
    """
    if amount_min != 'N/A' and amount_max != 'N/A':
        try:
            min_val = float(amount_min)
            max_val = float(amount_max)
            return f"${min_val:,.0f} - ${max_val:,.0f}"
        except:
            pass
    elif amount_max != 'N/A':
        try:
            max_val = float(amount_max)
            return f"Upp till ${max_val:,.0f}"
        except:
            pass
    return "Belopp ej angivet"

def format_date(date_str):
    """
    Formaterar datum på ett läsbart sätt
    """
    if date_str and date_str != 'N/A':
        try:
            # Försök parsa datum (format kan variera)
            if 'T' in date_str:
                date_str = date_str.split('T')[0]
            return date_str
        except:
            return date_str
    return "Inget deadline angivet"

def query_grants(query, k=5, verbose=True):
    """
    Söker efter bidrag baserat på en användarfråga
    
    Args:
        query: Användarens sökfråga
        k: Antal resultat att returnera
        verbose: Om True, visa detaljerad information
    
    Returns:
        Lista med matchande bidrag
    """
    if index.ntotal == 0:
        print("FAISS-indexet är tomt.")
        return []
    
    # Skapa embedding för frågan
    query_embedding = create_query_embedding(query)
    
    # Sök i indexet
    distances, indices = index.search(np.array(query_embedding), k=min(k, index.ntotal))
    
    # Hämta matchande bidrag
    matched_grants = []
    for i, (idx, distance) in enumerate(zip(indices[0], distances[0])):
        if 0 <= idx < len(grants_data):
            grant = grants_data[idx].copy()
            grant['match_score'] = float(distance)
            grant['rank'] = i + 1
            matched_grants.append(grant)
    
    return matched_grants

def display_results(query, results):
    """
    Visar sökresultat på ett snyggt sätt
    """
    print("\n" + "="*80)
    print(f"SÖKRESULTAT FÖR: '{query}'")
    print("="*80)
    
    if not results:
        print("\n❌ Inga bidrag hittades.")
        return
    
    print(f"\n✅ Hittade {len(results)} matchande bidrag:\n")
    
    for grant in results:
        print(f"{'─'*80}")
        print(f"#{grant['rank']}. {grant['title']}")
        print(f"{'─'*80}")
        print(f"📋 ID: {grant['number']}")
        print(f"🏛️  Myndighet: {grant['agency']}")
        print(f"💰 Belopp: {format_amount(grant['amount_min'], grant['amount_max'])}")
        print(f"📅 Sista ansökningsdag: {format_date(grant['deadline'])}")
        print(f"🏷️  Kategori: {grant['category']}")
        
        # Visa de första 200 tecknen av beskrivningen
        description = grant['description']
        if len(description) > 200:
            description = description[:200] + "..."
        print(f"📝 Beskrivning: {description}")
        
        print(f"🔗 Länk: {grant['url']}")
        print()
    
    print("="*80)

if __name__ == "__main__":
    # Interaktivt läge
    print("\n" + "="*80)
    print("GRANTS.GOV DEMO - INTELLIGENT BIDRAGSSÖKNING")
    print("="*80)
    print("\nBeskriv vad du söker bidrag för (på engelska för bäst resultat)")
    print("Exempel:")
    print("  - 'funding for education and youth programs'")
    print("  - 'environmental protection and climate change'")
    print("  - 'community health and wellness initiatives'")
    print("\nSkriv 'exit' för att avsluta\n")
    
    while True:
        try:
            query = input("🔍 Din fråga: ").strip()
            
            if not query:
                continue
            
            if query.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Tack för att du testade demon!")
                break
            
            # Sök och visa resultat
            results = query_grants(query, k=5)
            display_results(query, results)
            
            print("\n")
        
        except KeyboardInterrupt:
            print("\n\n👋 Tack för att du testade demon!")
            break
        except Exception as e:
            print(f"\n❌ Ett fel uppstod: {str(e)}\n")

