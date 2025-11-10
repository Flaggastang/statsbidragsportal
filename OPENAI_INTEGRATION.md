# 🤖 OpenAI GPT Integration

## Översikt

Detta dokument beskriver hur OpenAI GPT har integrerats i statsbidragsportalen för att skapa en **intelligent konversationsassistent**.

---

## 🎯 Två implementationer

### **Alternativ 1: Hybrid (Rekommenderad)** ✅

**Fil:** `demo_openai.py`

**Arkitektur:**
```
Användare → GPT (förstår fråga) → FAISS (söker) → GPT (analyserar) → Svar
```

**Fördelar:**
- ✅ Snabb sökning (FAISS, lokal)
- ✅ Intelligent konversation (GPT)
- ✅ Kostnadseffektiv (GPT används endast för analys)
- ✅ Fungerar offline efter indexering

**Kostnad:** ~$0.001-0.005 per sökning med GPT-4o-mini

---

### **Alternativ 2: Endast OpenAI Embeddings**

**Arkitektur:**
```
Användare → OpenAI Embeddings → FAISS → Resultat
```

**Fördelar:**
- ✅ Bättre embeddings än Sentence Transformers
- ✅ Stöd för 100+ språk

**Nackdelar:**
- ❌ Kräver API-anrop för varje indexering
- ❌ Kostnad per embedding
- ❌ Långsammare (nätverk)

**Vi rekommenderar INTE detta** eftersom:
- Sentence Transformers fungerar redan utmärkt
- OpenAI embeddings kostar pengar
- FAISS-sökningen är snabbast lokalt

---

## 🚀 Kom igång med GPT-integration

### Steg 1: Installera OpenAI SDK

```bash
pip install openai
```

### Steg 2: Få en API-nyckel

1. Gå till https://platform.openai.com/api-keys
2. Skapa ett konto (behöver betalkort)
3. Skapa en ny API-nyckel
4. Kopiera nyckeln (börjar med `sk-...`)

### Steg 3: Sätt API-nyckel

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="sk-din-nyckel-här"
```

**Mac/Linux:**
```bash
export OPENAI_API_KEY="sk-din-nyckel-här"
```

**Permanent (Mac/Linux):**
```bash
echo 'export OPENAI_API_KEY="sk-din-nyckel-här"' >> ~/.bashrc
source ~/.bashrc
```

### Steg 4: Kör GPT-demon

```bash
python demo_openai.py
```

---

## 💡 Vad GPT tillför

### **Utan GPT (Nuvarande):**
```
Användare: "innovation"
System: [Returnerar 5 bidrag]
```

### **Med GPT (Nytt):**
```
Användare: "Vi vill satsa på innovation och digitalisering i vår kommun"

GPT: "Jag hittade flera relevanta bidrag för er!

De mest relevanta är:

1. **STEM Education Innovation Fund** - Detta passar perfekt för 
   kommuner som vill utveckla innovationsförmågan. Särskilt bra 
   för utbildningsinsatser inom teknik och digitalisering.

2. **Technology Innovation and Workforce Development** - Fokuserar 
   på arbetsmarknadsutveckling inom digitala områden. Bra om ni 
   vill kombinera innovation med kompetensutveckling.

Vill ni fokusera mer på utbildning eller näringslivsutveckling? 
Det kan hjälpa mig ge bättre rekommendationer."
```

---

## 🎓 Demo-scenarion

### Scenario 1: Innovation & teknologi
```
Kommun: "Vi är en mindre kommun som vill satsa på innovation och 
        digitalisering. Finns det något för oss?"

GPT: [Analyserar behov]
     → Söker: "innovation technology digital transformation"
     → Hittar 5 bidrag
     → Rekommenderar de 2 bästa
     → Förklarar varför de passar
     → Frågar om kommun vill veta mer
```

### Scenario 2: Psykisk hälsa
```
Kommun: "Vi ser ökande behov av insatser för ungas psykiska hälsa"

GPT: [Förstår målgrupp och område]
     → Söker: "youth mental health wellness programs"
     → Analyserar resultat
     → Prioriterar bidrag för ungdomar
     → Föreslår kompletterande bidrag
```

---

## 📊 Kostnadsanalys

### GPT-4o-mini (Rekommenderad)

| Användning | Pris | Kostnad per sökning |
|------------|------|---------------------|
| Input | $0.150 / 1M tokens | ~$0.0003 |
| Output | $0.600 / 1M tokens | ~$0.0012 |
| **Total** | | **~$0.0015** |

**Årlig kostnad (1000 sökningar/månad):**
- 12,000 sökningar × $0.0015 = **$18/år**

### GPT-4 (Om bättre kvalitet behövs)

| Användning | Pris | Kostnad per sökning |
|------------|------|---------------------|
| Input | $5 / 1M tokens | ~$0.010 |
| Output | $15 / 1M tokens | ~$0.030 |
| **Total** | | **~$0.040** |

**Årlig kostnad (1000 sökningar/månad):**
- 12,000 sökningar × $0.040 = **$480/år**

**Rekommendation:** Börja med GPT-4o-mini, uppgradera endast om kvaliteten inte räcker.

---

## 🔧 Teknisk implementation

### Systemarkitektur

```python
# 1. Användare ställer fråga
user_message = "Vi behöver hjälp med integration"

# 2. GPT förstår och formulerar sökfråga
gpt_response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Du är en bidragsexpert..."},
        {"role": "user", "content": user_message}
    ]
)
search_query = gpt_response.choices[0].message.content

# 3. FAISS söker (snabbt, lokalt)
results = query_grants(search_query, k=5)

# 4. GPT analyserar och svarar
final_response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": f"Analysera: {results}"},
        {"role": "user", "content": user_message}
    ]
)
```

### Systemmeddelande (System Prompt)

```python
SYSTEM_PROMPT = """Du är en hjälpsam assistent för svenska kommuner 
som söker statsbidrag.

Din uppgift:
1. Hjälpa användaren formulera vad de söker
2. Analysera sökresultat och förklara vilka som passar bäst
3. Ställa uppföljningsfrågor för att förstå behoven bättre
4. Ge konkreta rekommendationer

Kommunicera på svenska och var professionell men tillgänglig.
"""
```

---

## 💡 Best Practices

### 1. Konversationshistorik

Spara hela konversationen för bättre kontext:

```python
conversation_history = [
    {"role": "user", "content": "Jag söker innovationsbidrag"},
    {"role": "assistant", "content": "Jag hittade 3 bidrag..."},
    {"role": "user", "content": "Berätta mer om det första"},
    # GPT kommer ihåg kontext!
]
```

### 2. Temperatur-inställning

```python
# Sökfråge-formulering (behöver precision)
temperature=0.3  # Låg = mer deterministisk

# Konversation (behöver kreativitet)
temperature=0.7  # Medel = balanserad
```

### 3. Token-optimering

```python
# Begränsa beskrivningslängd för att spara tokens
description = grant['description'][:200] + "..."

# Använd max_tokens för att kontrollera svarslängd
max_tokens=800  # Lagom för en rekommendation
```

### 4. Felhantering

```python
try:
    response = client.chat.completions.create(...)
except openai.RateLimitError:
    print("För många förfrågningar, vänta en stund")
except openai.APIError as e:
    print(f"API-fel: {e}")
```

---

## 🎯 Produktionisering

### För webbapp

```python
# FastAPI endpoint
@app.post("/api/search")
async def search_grants(request: SearchRequest):
    # 1. Validera input
    if len(request.message) > 500:
        raise HTTPException(400, "Meddelande för långt")
    
    # 2. Sök med GPT
    response, results = search_with_gpt(
        request.message,
        request.conversation_history
    )
    
    # 3. Returnera svar
    return {
        "response": response,
        "results": results,
        "conversation_id": request.conversation_id
    }
```

### Caching för vanliga frågor

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_search(query_hash):
    """Cachar vanliga sökningar"""
    return search_with_gpt(query)
```

### Rate limiting

```python
from ratelimit import limits

@limits(calls=100, period=3600)  # 100 anrop/timme
def search_with_gpt_limited(message):
    return search_with_gpt(message)
```

---

## 🆚 Jämförelse: Med vs Utan GPT

| Aspekt | Utan GPT | Med GPT |
|--------|----------|---------|
| **Sökmetod** | Direkt FAISS-sökning | GPT → FAISS → GPT |
| **Användarupplevelse** | Teknisk, direkt | Konversationell, hjälpsam |
| **Följdfrågor** | Nej | Ja |
| **Förklaringar** | Nej | Ja, detaljerade |
| **Kostnad** | Gratis | ~$18/år (1000 sök/mån) |
| **Responstid** | <100ms | ~2-3 sekunder |
| **Kontext** | Ingen | Hela konversationen |
| **Personalisering** | Nej | Ja |

---

## 🎓 Exempel på interaktion

### Scenario: En kommun söker integrationsstöd

```
──────────────────────────────────────────────────────────
💬 Användare:
"Vi har fått många nyanlända och behöver stöd för integration 
och språkundervisning. Vad finns?"

🤖 GPT-assistent:
"Jag förstår att ni söker stöd för integration och språkträning 
för nyanlända. Låt mig söka efter relevanta bidrag...

🔍 Jag hittade flera intressanta möjligheter:

**Mest relevanta för er:**

1. Community Development and Social Services Grant
   • Fokuserar på integration och samhällstjänster
   • Passar perfekt för nyanlända
   • Deadline: 2025-07-15
   • Belopp: $150,000 - $2,000,000

2. Education Excellence Grant for Underserved Youth
   • Kan användas för språkundervisning
   • Riktar sig mot utsatta grupper
   • Deadline: 2025-03-15

**Min rekommendation:**
Börja med bidrag #1 då det direkt täcker integration. Bidrag #2 
kan komplettera om ni vill fokusera på språkträning för barn.

Vill ni att jag berättar mer om ansökningsprocessen eller har ni 
andra behov som jag kan hjälpa er med?"

💬 Användare:
"Ja, berätta mer om ansökningsprocessen för det första"

🤖 GPT-assistent:
[Fortsätter konversationen med kontextförståelse...]
──────────────────────────────────────────────────────────
```

---

## 📈 Nästa steg

### Fas 1: Testa (NU)
- [x] ✅ Kör `demo_openai.py`
- [x] ✅ Testa olika frågor
- [ ] ⏳ Samla feedback från användare

### Fas 2: Förfina
- [ ] Optimera system-prompt
- [ ] Lägg till fler exempel i prompts
- [ ] Implementera caching
- [ ] A/B-testa med och utan GPT

### Fas 3: Produktionisera
- [ ] FastAPI backend
- [ ] React frontend med chattgränssnitt
- [ ] Databas för konversationshistorik
- [ ] Analytics för vanliga frågor
- [ ] Rate limiting och monitoring

---

## 🔒 Säkerhet & Privacy

### API-nyckelhantering

```python
# Aldrig hardcoda nycklar!
# ❌ DÅLIGT
api_key = "sk-1234567890"

# ✅ BRA
api_key = os.getenv("OPENAI_API_KEY")
```

### Datahantering

OpenAI's policy (från mars 2023):
- ✅ Data från API skickas INTE för träning (om opt-out aktiverat)
- ✅ Sparas i 30 dagar för missbrukskontroll
- ✅ Raderas sedan automatiskt

**För produktion:** Verifiera alltid senaste policyn och GDPR-compliance.

---

## 💰 Kostnadskontroll

### Sätt budgetar i OpenAI Dashboard

1. Gå till https://platform.openai.com/account/billing/limits
2. Sätt "Hard limit" (t.ex. $50/månad)
3. Aktivera e-postaviseringar

### Monitora användning

```python
import openai

# Logga varje API-anrop
def log_usage(model, tokens_used, cost):
    print(f"Model: {model}, Tokens: {tokens_used}, Cost: ${cost:.4f}")
```

---

## 📚 Resurser

- [OpenAI API Dokumentation](https://platform.openai.com/docs)
- [GPT-4o-mini Pricing](https://openai.com/pricing)
- [Best Practices för Prompts](https://platform.openai.com/docs/guides/prompt-engineering)
- [OpenAI Python SDK](https://github.com/openai/openai-python)

---

## 🤝 Bidra

Har du idéer för att förbättra GPT-integrationen?
- Öppna ett Issue på GitHub
- Skicka en Pull Request
- Dela dina erfarenheter

---

**Skapad:** 2024-11-10  
**Senast uppdaterad:** 2024-11-10  
**Status:** ✅ Fungerande demo

