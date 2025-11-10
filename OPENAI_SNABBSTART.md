# 🤖 Snabbstart: GPT-assistent

## 3 steg till intelligent bidragssökning

### Steg 1: Få en OpenAI API-nyckel (5 minuter)

1. Gå till https://platform.openai.com/signup
2. Skapa konto (behöver betalkort)
3. Gå till https://platform.openai.com/api-keys
4. Klicka "Create new secret key"
5. Kopiera nyckeln (börjar med `sk-...`)

💰 **Kostnad:** ~$18/år för 1000 sökningar/månad (med GPT-4o-mini)

---

### Steg 2: Sätt API-nyckel

**Windows PowerShell:**
```powershell
$env:OPENAI_API_KEY="sk-din-nyckel-här"
```

**Mac/Linux:**
```bash
export OPENAI_API_KEY="sk-din-nyckel-här"
```

**Verifiera:**
```bash
echo $env:OPENAI_API_KEY  # Windows
echo $OPENAI_API_KEY       # Mac/Linux
```

---

### Steg 3: Kör GPT-demon

```bash
# Installera OpenAI (om du inte redan gjort det)
pip install openai

# Kör demon
python demo_openai.py
```

**Välj läge:**
- **1** = Demo med förberedda scenarion (rekommenderat första gången)
- **2** = Interaktiv chatt (ställ egna frågor)

---

## 🎭 Testa dessa frågor:

### På svenska:
- "Vi behöver stöd för integration av nyanlända"
- "Hur kan vi finansiera cykelvägar och hållbar transport?"
- "Finns det bidrag för ungas psykiska hälsa?"
- "Vi vill satsa på digital kompetens i skolan"

### På engelska:
- "funding for innovation and technology"
- "community health programs"
- "environmental sustainability projects"

---

## 💡 Vad är skillnaden?

### Utan GPT (`demo_quick.py`):
```
Du: "innovation"
System: [5 bidrag visas]
```

### Med GPT (`demo_openai.py`):
```
Du: "Vi vill satsa på innovation"

GPT: "Jag förstår att ni söker innovationsstöd! 
     Här är de bästa alternativen:
     
     1. STEM Education Innovation Fund
        → Perfekt för utbildningsinsatser inom innovation
        → Deadline: 2025-06-01
        → Rekommenderar jag starkt!
     
     2. Technology Innovation and Workforce Development
        → Bra om ni vill kombinera med kompetensutveckling
     
     Vill ni fokusera mer på utbildning eller näringsliv?"
```

---

## 🎯 Fördelar med GPT:

✅ **Förstår kontext** - "Vi har många nyanlända" → söker integration  
✅ **Ställer följdfrågor** - "Vill ni fokusera på barn eller vuxna?"  
✅ **Förklarar varför** - "Detta passar er eftersom..."  
✅ **Kommer ihåg** - Hela konversationen sparas  
✅ **Personligt** - Anpassar svar efter er situation  

---

## 💰 Kostnadskontroll

### Sätt budget i OpenAI Dashboard:

1. Gå till https://platform.openai.com/account/billing/limits
2. Sätt "Hard limit" till t.ex. $50/månad
3. Aktivera e-postaviseringar

### Uppskattad användning:

| Användning | Kostnad/månad |
|------------|---------------|
| 100 sökningar | $0.15 |
| 500 sökningar | $0.75 |
| 1000 sökningar | $1.50 |
| 5000 sökningar | $7.50 |

*Med GPT-4o-mini (rekommenderad)*

---

## 🔒 Säkerhet

**Viktigt:**
- ❌ Dela ALDRIG din API-nyckel
- ❌ Committa ALDRIG nyckeln till Git
- ✅ Använd environment-variabler
- ✅ Sätt utgångsdatum på nycklar

**Rotera nycklar regelbundet:**
1. Skapa ny nyckel
2. Uppdatera i systemet
3. Ta bort gammal nyckel

---

## 🐛 Felsökning

### Problem: "OPENAI_API_KEY saknas"

**Lösning:**
```bash
# Sätt nyckeln igen
$env:OPENAI_API_KEY="sk-..."  # Windows
export OPENAI_API_KEY="sk-..."  # Mac/Linux
```

### Problem: "RateLimitError"

**Lösning:**
- Du har gjort för många anrop
- Vänta 1 minut och försök igen
- Eller uppgradera ditt konto

### Problem: "Insufficient quota"

**Lösning:**
- Ditt konto saknar kredit
- Lägg till betalkort i OpenAI Dashboard
- Eller öka din spending limit

---

## 📊 Jämförelse med andra lösningar

| Lösning | Kostnad | Intelligens | Responstid |
|---------|---------|-------------|------------|
| **Nuvarande (FAISS)** | Gratis | ⭐⭐⭐ | <100ms |
| **+ GPT-4o-mini** | $1.50/mån* | ⭐⭐⭐⭐⭐ | 2-3s |
| **+ GPT-4** | $40/mån* | ⭐⭐⭐⭐⭐⭐ | 3-5s |
| **Endast OpenAI Embeddings** | $5/mån* | ⭐⭐⭐⭐ | 500ms |

*För 1000 sökningar/månad

**Rekommendation:** Hybrid med GPT-4o-mini (bästa balansen)

---

## 🚀 Nästa steg

1. ✅ Testa GPT-demon (`python demo_openai.py`)
2. ✅ Jämför med vanlig sökning (`python demo_quick.py`)
3. ✅ Samla feedback från kollegor
4. ✅ Besluta om GPT ska användas i produktion

---

## 💬 Support

**Frågor?**
- Läs [OPENAI_INTEGRATION.md](OPENAI_INTEGRATION.md) för detaljer
- Öppna ett Issue på GitHub
- Kontakta projektansvarig

---

**Lycka till med din intelligenta bidragsassistent!** 🚀

