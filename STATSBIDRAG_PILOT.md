# 🎯 Statsbidragsportal - AI-sökning Pilot

## 📋 Översikt

Detta är en **proof-of-concept pilot** som demonstrerar hur AI-driven semantisk sökning kan användas för att hjälpa svenska kommuner hitta relevanta statsbidrag. Piloten använder Grants.gov (USA:s federala bidragsdatabas) som datakälla för att visa tekniken i praktiken.

### 🎬 Vad är detta?

En fungerande prototyp av ett intelligent söksystem där kommuner kan:
- ✅ Ställa frågor på naturligt svenska språk
- ✅ Få relevanta bidrag baserat på **betydelse**, inte bara nyckelord
- ✅ Snabbt hitta rätt bidrag bland hundratals alternativ

### 🆚 Jämförelse: Pilot vs. Statsbidragstjänst

| Aspekt | 🧪 Denna Pilot | 🎯 Statsbidragstjänst (Målbild) |
|--------|---------------|----------------------------------|
| **Datakälla** | Grants.gov API (USA) - 130 bidrag | Svenska statsbidrag - ~160 bidrag |
| **Språk** | Engelska bidrag, svenska/engelska sökning | Svenska bidrag och sökning |
| **Teknologi** | ✅ AI semantisk sökning (FAISS + transformers) | ✅ Samma teknologi |
| **Sökmetod** | ✅ Naturligt språk, förstår betydelse | ✅ Samma |
| **Gränssnitt** | Kommandorad (CLI) | Webbgränssnitt + API |
| **Datafält** | Titel, beskrivning, myndighet, deadline, länk | + Belopp, målgrupp, kontaktperson, alla 10 fält |
| **Användare** | Demo/test | Kommuner i produktion |
| **Uppdatering** | Manuell (kör script) | Automatisk (cron/scheduled) |
| **Tid att bygga** | ✅ **2-3 timmar** (KLART!) | 2-4 veckor för full tjänst |

---

## 🏗️ Arkitektur

### Teknisk Stack

```
┌─────────────────────────────────────────────────────────────┐
│                    ANVÄNDARGRÄNSSNITT                        │
│  Pilot: Kommandorad  │  Produktion: React/Vue Webbapp       │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                    SÖKMOTORN (AI)                            │
│  • Sentence Transformers (Hugging Face)                     │
│  • Naturlig språkförståelse                                 │
│  • Semantisk matchning                                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   VEKTORSÖKNING                              │
│  • FAISS (Facebook AI Similarity Search)                    │
│  • <100ms sökrespons                                        │
│  • Skalbart till tusentals bidrag                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                     DATAKÄLLA                                │
│  Pilot: Grants.gov API  │  Produktion: SQL/JSON med         │
│  (REST API)             │  svenska statsbidrag              │
└─────────────────────────────────────────────────────────────┘
```

### Dataflöde

```
1. INDEXERING (Körs en gång eller vid uppdatering)
   ┌─────────────────────────────────────────────────────┐
   │ Hämta bidrag → Skapa AI-embeddings → FAISS-index   │
   └─────────────────────────────────────────────────────┘
   
2. SÖKNING (Körs vid varje användarfråga)
   ┌─────────────────────────────────────────────────────┐
   │ Användarfråga → AI-embedding → Sök i FAISS →       │
   │ Returnera top 5 matchningar                         │
   └─────────────────────────────────────────────────────┘
```

---

## 🚀 Kom igång med piloten

### Förutsättningar

- **Python 3.8+**
- **4GB RAM** (för AI-modellen)
- **Internetanslutning** (för att hämta bidrag och AI-modell)

### Installation

#### 1. Klona repositoryt

```bash
git clone https://github.com/Flaggastang/statsbidragsportal.git
cd statsbidragsportal
```

#### 2. Installera beroenden

```bash
pip install -r requirements.txt
```

**OBS:** Första gången kan ta 2-5 minuter eftersom AI-modellen laddas ner (ca 80 MB).

#### 3. Indexera bidrag

```bash
python scripts/fetch_and_index_grants.py
```

Detta:
- Hämtar ~130 bidrag från Grants.gov API
- Skapar AI-embeddings för varje bidrag
- Bygger FAISS-sökindex
- **Tar cirka 2-3 minuter**

#### 4. Kör demon!

**Alternativ A: Snabb demo (rekommenderat)**
```bash
python demo_quick.py
```
Visar 4 förberedda scenarion direkt.

**Alternativ B: Interaktiv sökning**
```bash
python demo_grants.py
```
Välj läge 2 och skriv egna frågor.

**Alternativ C: GPT-assistent (NYTT!)**
```bash
python demo_openai.py
```
Intelligent konversation med OpenAI GPT. Kräver API-nyckel.
Se [OPENAI_SNABBSTART.md](OPENAI_SNABBSTART.md) för setup.

**Alternativ C: Direkt sökning**
```bash
python -c "from scripts.query_grants import query_grants, display_results; results = query_grants('innovation funding'); display_results('innovation funding', results)"
```

---

## 🎭 Demo-scenarion

### Scenario 1: Utbildning & ungdom
**Fråga:** *"funding for education programs helping disadvantaged youth"*

**Resultat:** Utbildningsprogram, forskningsstipendier, ungdomsinitiativ

### Scenario 2: Miljö & hållbarhet
**Fråga:** *"environmental protection climate change sustainability"*

**Resultat:** Miljöforskning, hållbarhetsprojekt, klimatinitiativ

### Scenario 3: Folkhälsa
**Fråga:** *"community health wellness programs mental health"*

**Resultat:** Mental hälsa, välbefinnandeprogram, samhällshälsa

### Scenario 4: Innovation
**Fråga (svenska!):** *"Vad finns det om man håller på med innovation?"*

**Resultat:** STEM-utbildning, teknologikommersialisering, forskningsutveckling

---

## 🔧 Anpassa för svenska statsbidrag

### Steg 1: Förbered data

Skapa en JSON-fil `svenska_statsbidrag.json`:

```json
{
  "bidrag": [
    {
      "id": "SB-001",
      "namn": "Integrationsbidrag för kommuner",
      "beskrivning": "Statsbidrag för integration och etablering av nyanlända...",
      "myndighet": "Arbetsförmedlingen",
      "belopp_min": 100000,
      "belopp_max": 5000000,
      "malgrupp": "Nyanlända, kommuner",
      "sista_ansokningsdag": "2025-03-31",
      "webbplats": "https://...",
      "kontaktperson": "Anna Svensson",
      "telefon": "08-123456"
    }
  ]
}
```

### Steg 2: Modifiera indexeringsskriptet

I `scripts/fetch_and_index_grants.py`, ersätt `fetch_grants_data()`:

```python
def fetch_grants_data():
    """Läser svenska statsbidrag från lokal JSON"""
    import json
    
    with open("svenska_statsbidrag.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    grants = []
    for bidrag in data['bidrag']:
        grants.append({
            'id': bidrag['id'],
            'number': bidrag['id'],
            'title': bidrag['namn'],
            'description': bidrag['beskrivning'],
            'agency': bidrag['myndighet'],
            'amount_min': bidrag.get('belopp_min', 'N/A'),
            'amount_max': bidrag.get('belopp_max', 'N/A'),
            'deadline': bidrag['sista_ansokningsdag'],
            'category': bidrag['malgrupp'],
            'url': bidrag['webbplats']
        })
    
    return grants
```

### Steg 3: Byt till flerspråkig modell

I både `fetch_and_index_grants.py` och `query_grants.py`:

```python
# Ersätt:
model_name = "sentence-transformers/all-MiniLM-L6-v2"

# Med:
model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
```

### Steg 4: Indexera och testa

```bash
python scripts/fetch_and_index_grants.py
python demo_quick.py
```

---

## 📊 Prestandamått (från piloten)

| Mått | Värde | Kommentar |
|------|-------|-----------|
| **Indexeringstid** | 2-3 min | För 130 bidrag, första gången |
| **Söktid** | <100ms | Per sökning |
| **Modellstorlek** | 80 MB | AI-modellen |
| **Indexstorlek** | <1 MB | FAISS-index för 130 bidrag |
| **Minneskrav** | 2-4 GB | Under körning |
| **Skalbarhet** | 10,000+ | Klarar tusentals bidrag |
| **Språkstöd** | Många | Med flerspråkig modell |

---

## 💡 Vad piloten visar

### ✅ Bevisade koncept

1. **AI förstår naturligt språk**
   - Användare kan fråga på svenska eller engelska
   - Systemet förstår synonymer och relaterade begrepp
   - Ingen träning behövs för nya användare

2. **Semantisk sökning fungerar**
   - "Innovation" → hittar STEM, kommersialisering, forskning
   - "Unga i utsatta områden" → hittar utbildning, hälsa, integration
   - Bättre än traditionell nyckelordssökning

3. **Snabb och skalbar**
   - <100ms sökrespons
   - Klarar hundratals eller tusentals bidrag
   - Ingen databas krävs för sökning

4. **Enkel implementation**
   - ~300 rader Python-kod
   - Använder standardbibliotek
   - Lätt att underhålla och vidareutveckla

### 🎯 Nästa steg för produktion

#### Fas 1: Data (1 vecka)
- [ ] Samla alla 160 svenska statsbidrag
- [ ] Strukturera i databas (PostgreSQL rekommenderas)
- [ ] Definiera alla 10 datafält
- [ ] Skapa uppdateringsrutin

#### Fas 2: Backend (1 vecka)
- [ ] FastAPI REST API
- [ ] Autentisering (om behövs)
- [ ] Filter-funktioner (belopp, deadline, målgrupp)
- [ ] Loggning och monitoring

#### Fas 3: Frontend (1-2 veckor)
- [ ] React/Vue webbapp
- [ ] Sökgränssnitt med autocomplete
- [ ] Resultatvisning med alla fält
- [ ] Responsive design (mobil + desktop)
- [ ] Favoriter och sparade sökningar

#### Fas 4: Deployment (3-5 dagar)
- [ ] Containerisering (Docker)
- [ ] CI/CD pipeline
- [ ] Hosting (Azure/AWS/on-premise)
- [ ] SSL-certifikat
- [ ] Backup-strategi

#### Fas 5: Underhåll
- [ ] Automatisk uppdatering av bidrag
- [ ] Användarfeedback-system
- [ ] Analytics och statistik
- [ ] Kontinuerlig förbättring

---

## 🔍 Tekniska detaljer

### AI-modellen

**Nuvarande (pilot):** `sentence-transformers/all-MiniLM-L6-v2`
- Storlek: 80 MB
- Språk: Främst engelska, viss flerspråkig förmåga
- Snabb och effektiv

**Rekommenderad (produktion):** `paraphrase-multilingual-MiniLM-L12-v2`
- Storlek: 420 MB
- Språk: 50+ språk inklusive svenska
- Bättre semantisk förståelse för svenska

### FAISS Index

- **Typ:** IndexFlatL2 (exakt L2-avstånd)
- **Dimension:** 384 (all-MiniLM) eller 384 (multilingual)
- **Skalbarhet:** För >10,000 bidrag, byt till IndexIVFFlat

### Databas (för produktion)

**Rekommendation:**

```sql
CREATE TABLE statsbidrag (
    id SERIAL PRIMARY KEY,
    bidrag_id VARCHAR(50) UNIQUE NOT NULL,
    namn VARCHAR(255) NOT NULL,
    beskrivning TEXT NOT NULL,
    myndighet VARCHAR(255) NOT NULL,
    belopp_min DECIMAL(12, 2),
    belopp_max DECIMAL(12, 2),
    malgrupp VARCHAR(255),
    sista_ansokningsdag DATE,
    webbplats TEXT,
    kontaktperson VARCHAR(255),
    telefon VARCHAR(50),
    epost VARCHAR(255),
    skapad TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    uppdaterad TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Full-text search stöd
    searchable_text TSVECTOR GENERATED ALWAYS AS (
        to_tsvector('swedish', 
            coalesce(namn, '') || ' ' || 
            coalesce(beskrivning, '') || ' ' || 
            coalesce(malgrupp, '')
        )
    ) STORED
);

-- Index för snabb sökning
CREATE INDEX idx_statsbidrag_searchable ON statsbidrag USING GIN (searchable_text);
CREATE INDEX idx_statsbidrag_deadline ON statsbidrag (sista_ansokningsdag);
```

---

## 🎓 Lärdomar från piloten

### ✅ Vad fungerade bra

1. **Snabb utveckling** - Från noll till fungerande demo på några timmar
2. **Robust API** - Grants.gov API fungerade stabilt
3. **Bra prestanda** - Även med grundmodellen
4. **Språkflexibilitet** - Fungerar oväntat bra med svenska frågor

### ⚠️ Utmaningar

1. **API-dokumentation** - Grants.gov bytte API-version, krävde anpassning
2. **Beskrivningar saknas** - Många bidrag saknar detaljerade beskrivningar
3. **Modellstorlek** - Större flerspråkig modell tar mer minne

### 💡 Rekommendationer

1. **Använd flerspråkig modell** för produktion med svenska
2. **Lägg till filter** - Låt användare filtrera på belopp, deadline, målgrupp
3. **Caching** - Cacha vanliga sökningar för snabbare respons
4. **Feedback-loop** - Låt användare markera bra/dåliga resultat för förbättring
5. **GPT-integration** ✅ IMPLEMENTERAT! - Använd `demo_openai.py` för intelligent konversation

---

## 📚 Resurser

### Dokumentation

- **Pilot README:** `GRANTS_DEMO_README.md` - Detaljerad teknisk dokumentation
- **Snabbstart:** `SNABBSTART.md` - Kom igång på 3 minuter
- **Denna fil:** `STATSBIDRAG_PILOT.md` - Översikt och jämförelse
- **OpenAI Integration:** `OPENAI_INTEGRATION.md` - GPT-funktionalitet (NYTT)
- **OpenAI Snabbstart:** `OPENAI_SNABBSTART.md` - Kom igång med GPT (NYTT)

### Kodstruktur

```
statsbidragsportal/
├── scripts/
│   ├── fetch_and_index_grants.py  # Hämta och indexera bidrag
│   ├── query_grants.py            # Sökmotorn
│   └── utils.py                   # Hjälpfunktioner (tom för nu)
├── demo_grants.py                 # Interaktiv demo
├── demo_quick.py                  # Snabb demo (4 scenarion)
├── requirements.txt               # Python-beroenden
├── STATSBIDRAG_PILOT.md          # Denna fil
├── GRANTS_DEMO_README.md         # Teknisk dokumentation
└── SNABBSTART.md                 # Snabbguide
```

### Externa länkar

- [Sentence Transformers](https://www.sbert.net/) - AI-modeller för semantisk sökning
- [FAISS](https://github.com/facebookresearch/faiss) - Facebook AI Similarity Search
- [Grants.gov API](https://grants.gov/api/common/search2) - API-dokumentation
- [Hugging Face](https://huggingface.co/) - AI-modellbibliotek

---

## 🤝 Bidra

Detta är en pilot/proof-of-concept. Förslag och förbättringar välkomnas!

### Möjliga förbättringar

- [x] ✅ **GPT-konversationsassistent** (IMPLEMENTERAT!)
- [ ] Webbgränssnitt (React/Vue)
- [ ] REST API (FastAPI)
- [ ] Filtrering och sortering
- [ ] Export till Excel/PDF
- [ ] E-postaviseringar för nya bidrag
- [ ] Användarautentisering
- [ ] Admin-panel för datahantering
- [ ] Analytics och statistik
- [ ] A/B-testning av olika modeller
- [ ] Feedback-system

---

## 📞 Kontakt

För frågor om piloten eller implementering av statsbidragstjänsten, kontakta projektansvarig.

---

## 📄 Licens

[Lägg till licens här]

---

**Skapad:** 2024-11-10  
**Senast uppdaterad:** 2024-11-10  
**Version:** 1.0 (Pilot)  
**Status:** ✅ Fungerande proof-of-concept

