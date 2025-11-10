# 🎯 Grants.gov Demo - Intelligent Bidragssökning

Detta är en demo som visar hur AI-driven semantisk sökning kan användas för att hjälpa kommuner hitta relevanta statsbidrag.

## 📋 Vad gör demon?

Systemet:
1. ✅ Hämtar aktuella bidrag från Grants.gov API (USA:s federala bidragsdatabas)
2. ✅ Använder AI (sentence-transformers) för att förstå betydelsen av bidragsbeskrivningar
3. ✅ Bygger ett sökindex med FAISS för snabb semantisk sökning
4. ✅ Låter användare söka med naturliga språkfrågor
5. ✅ Returnerar de mest relevanta bidragen baserat på BETYDELSE, inte bara nyckelord

## 🚀 Kom igång

### Steg 1: Installera beroenden

```bash
pip install -r requirements.txt
```

**OBS:** Första gången kan det ta några minuter eftersom AI-modellen laddas ner (ca 80 MB).

### Steg 2: Indexera bidrag (engångskörning)

```bash
python scripts/fetch_and_index_grants.py
```

Detta:
- Hämtar ~200 bidrag från Grants.gov
- Skapar AI-embeddings för varje bidrag
- Bygger ett FAISS-sökindex
- Tar cirka 2-3 minuter

**Filer som skapas:**
- `data/grants_index.faiss` - Sökindexet
- `data/grants_data.json` - Bidragsdata
- `data/grants_metadata.txt` - Metadata

### Steg 3: Kör demon

```bash
python demo_grants.py
```

**Välj mellan två lägen:**

**1. Demo-läge (rekommenderat för första körningen)**
- Kör förberedda scenarion
- Visar hur systemet fungerar i praktiken
- Perfekt för att visa för kollegor/kunder

**2. Interaktivt läge**
- Skriv egna frågor
- Testa systemet själv
- Exempel på frågor:
  - "funding for education programs helping disadvantaged youth"
  - "environmental protection climate change sustainability"
  - "community health wellness programs"

## 📊 Exempel på resultat

**Fråga:** *"funding for education programs helping disadvantaged youth"*

**Resultat:**
```
#1. Education Grants for At-Risk Youth
📋 ID: ED-GRANTS-2024-001
🏛️ Myndighet: Department of Education
💰 Belopp: $50,000 - $500,000
📅 Deadline: 2025-03-15
🏷️ Kategori: Education
🔗 Länk: [URL]
```

## 🎨 Hur anpassar jag detta för svenska statsbidrag?

### A. Med API/Databas

Modifiera `scripts/fetch_and_index_grants.py`:

```python
def fetch_grants_data():
    # Ersätt Grants.gov API med ert eget API
    url = "https://ert-api.se/statsbidrag"
    response = requests.get(url)
    
    # Anpassa till er datastruktur
    grants = []
    for item in response.json():
        grants.append({
            'id': item['id'],
            'title': item['namn'],
            'description': item['beskrivning'],
            'amount_max': item['belopp'],
            'deadline': item['sista_ansokningsdag'],
            'agency': item['myndighet'],
            'url': item['länk']
        })
    return grants
```

### B. Med JSON-fil

Om ni har data i en JSON-fil:

```python
def fetch_grants_data():
    with open("statsbidrag.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Returnera i rätt format
    return data['bidrag']
```

### C. Med SQL-databas

```python
import sqlite3

def fetch_grants_data():
    conn = sqlite3.connect('statsbidrag.db')
    cursor = conn.execute("""
        SELECT id, namn, beskrivning, belopp, 
               sista_ansokningsdag, myndighet, url
        FROM statsbidrag
    """)
    
    grants = []
    for row in cursor:
        grants.append({
            'id': row[0],
            'title': row[1],
            'description': row[2],
            # ... etc
        })
    
    return grants
```

## 🌐 Svensk språkstöd

För BÄSTA resultat på svenska, byt AI-modell:

```python
# I fetch_and_index_grants.py och query_grants.py
# Ersätt:
model_name = "sentence-transformers/all-MiniLM-L6-v2"

# Med en flerspråkig eller svenskoptimerad modell:
model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
```

## 🔧 Teknisk stack

- **Python 3.8+**
- **Requests** - API-anrop
- **Transformers** - AI-modeller från Hugging Face
- **PyTorch** - Maskininlärningsramverk
- **FAISS** - Snabb vektorsökning (Facebook AI)
- **NumPy** - Numeriska beräkningar

## 📈 Prestanda

- **Indexering:** ~2-3 minuter för 200 bidrag
- **Sökning:** <100ms per fråga
- **Skalbarhet:** Klarar tusentals bidrag utan problem

## 🎯 Nästa steg för produktionssystem

1. **Webbgränssnitt**
   - React/Vue frontend
   - FastAPI backend
   - REST API för sökning

2. **Databas-integration**
   - SQL för strukturerad data
   - Auto-uppdatering av index

3. **Avancerade funktioner**
   - Filtrera på datum, belopp, målgrupp
   - Favoriter och sparade sökningar
   - E-postaviseringar för nya bidrag

4. **LLM-integration (ChatGPT/Claude)**
   - Konversationsgränssnitt
   - Ställ följdfrågor
   - Få rekommendationer

## 🐛 Felsökning

**Problem:** "Kunde inte ladda FAISS-index"
- **Lösning:** Kör `python scripts/fetch_and_index_grants.py` först

**Problem:** "Failed to fetch data from Grants.gov"
- **Lösning:** Kontrollera internetanslutningen, API:et kan vara tillfälligt nere

**Problem:** "ModuleNotFoundError"
- **Lösning:** Kör `pip install -r requirements.txt`

## 💡 Frågor?

Detta är en proof-of-concept som visar hur AI-driven sökning fungerar.
Samma koncept kan appliceras på:
- ✅ Svenska statsbidrag
- ✅ Lagtexter och förordningar
- ✅ Policydokument
- ✅ Forskningsartiklar
- ✅ Jobbannoner
- ✅ Och mycket mer!

---

**Skapad:** 2024-11-10
**Baserad på:** Kolada KPI-matcher projektet

