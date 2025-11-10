# 🎯 Statsbidragsportal - AI-sökning (Pilot)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**En proof-of-concept som visar hur AI-driven semantisk sökning kan hjälpa svenska kommuner hitta relevanta statsbidrag.**

---

## 🚀 Snabbstart

```bash
# 1. Installera beroenden
pip install -r requirements.txt

# 2. Indexera bidrag (tar 2-3 minuter)
python scripts/fetch_and_index_grants.py

# 3. Kör demon!
python demo_quick.py
```

**Det var det!** Nu kan du se hur AI-sökning fungerar. ✨

---

## 💡 Vad är detta?

Detta är en **fungerande prototyp** som demonstrerar tekniken bakom en intelligent statsbidragssökning. 

### Så här fungerar det:

**Traditionell sökning:**
```
Användare söker: "integration"
Resultat: Bara bidrag med ordet "integration"
```

**AI-driven sökning (detta system):**
```
Användare frågar: "Vi behöver stöd för nyanlända"
Resultat: Hittar bidrag om integration, språkträning, 
         arbetsmarknad, etablering - även utan exakta ord!
```

### 🎬 Live demo

```bash
python demo_quick.py
```

**Exempel på sökningar som fungerar:**

| Fråga (svenska) | Vad AI hittar |
|-----------------|---------------|
| "Vi håller på med innovation" | STEM-utbildning, teknologikommersialisering, forskningsutveckling |
| "Miljö och hållbarhet" | Klimatprojekt, hållbarhetsforskning, miljöskydd |
| "Psykisk hälsa för unga" | Mental hälsa program, ungdomsstöd, välbefinnande |

---

## 📊 Pilot vs. Produktionssystem

| Funktion | 🧪 Denna Pilot | 🎯 Produktionsmål |
|----------|----------------|-------------------|
| Datakälla | Grants.gov (USA) | Svenska statsbidrag |
| Antal bidrag | ~130 | ~160 |
| Sökning | ✅ AI semantisk | ✅ AI semantisk |
| Språk | Svenska/Engelska | ✅ Svenska |
| Gränssnitt | Kommandorad | → Webbapp |
| Status | **✅ KLART** | 2-4 veckor |

---

## 🎯 För vem är detta?

### Kommuner som vill:
- 💰 Hitta rätt statsbidrag snabbare
- 🤖 Använda naturligt språk istället för nyckelord
- ⚡ Få svar på sekunder, inte timmar

### Utvecklare som vill:
- 🔍 Se hur semantisk sökning fungerar i praktiken
- 🧠 Förstå AI-driven matchning
- 🚀 Bygga liknande system

### Beslutsfattare som vill:
- 📈 Se en fungerande proof-of-concept
- 💡 Förstå tekniska möjligheter
- ✅ Bedöma genomförbarhet

---

## 📚 Dokumentation

- **[STATSBIDRAG_PILOT.md](STATSBIDRAG_PILOT.md)** - Komplett översikt och jämförelse
- **[GRANTS_DEMO_README.md](GRANTS_DEMO_README.md)** - Teknisk dokumentation
- **[SNABBSTART.md](SNABBSTART.md)** - Kom igång på 3 minuter

---

## 🏗️ Hur det fungerar (förenklat)

```
┌─────────────────────────────────────────────────┐
│  1. INDEXERING (görs en gång)                   │
│     Bidrag → AI-analys → Sökindex              │
└─────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────┐
│  2. SÖKNING (vid varje fråga)                   │
│     "innovation" → AI → Relevanta bidrag        │
│     <100ms sökrespons                           │
└─────────────────────────────────────────────────┘
```

### Teknisk stack:
- **Python 3.8+** - Programmeringsspråk
- **Sentence Transformers** - AI för textförståelse
- **FAISS** - Snabb vektorsökning (Facebook AI)
- **Grants.gov API** - Datakälla (kan bytas ut)

---

## 🔧 Anpassa för svenska statsbidrag

Se detaljerad guide i [STATSBIDRAG_PILOT.md](STATSBIDRAG_PILOT.md#-anpassa-för-svenska-statsbidrag)

**Kort version:**

1. Samla era statsbidrag i JSON/SQL
2. Ändra en funktion i `scripts/fetch_and_index_grants.py`
3. Byt till flerspråkig AI-modell
4. Kör indexering
5. **Klart!** ✨

---

## 🎓 Vad vi har lärt oss

### ✅ Fungerar bra:
- AI förstår svenska frågor (även med engelsktränad modell!)
- Semantisk matchning ger bättre resultat än nyckelord
- Snabbt och skalbart (klarar tusentals bidrag)
- Enkelt att implementera

### 💡 Rekommendationer för produktion:
- Använd flerspråkig modell för bättre svenskstöd
- Lägg till webbgränssnitt (React/Vue)
- Implementera filter (belopp, deadline, målgrupp)
- Automatisk uppdatering av bidrag

---

## 📊 Prestanda

| Mått | Värde |
|------|-------|
| Indexeringstid | 2-3 minuter (för 130 bidrag) |
| Söktid | <100ms per sökning |
| Modellstorlek | 80 MB |
| Minneskrav | 2-4 GB |
| Skalbarhet | 10,000+ bidrag |

---

## 🤝 Bidra

Detta är en proof-of-concept. Förslag och förbättringar välkomnas!

**Möjliga förbättringar:**
- [ ] Webbgränssnitt
- [ ] REST API
- [ ] Filtrering och sortering
- [ ] Export till Excel/PDF
- [ ] Användarkonton
- [ ] Admin-panel

---

## 📞 Support

**Problem?** Öppna ett [issue](https://github.com/Flaggastang/statsbidragsportal/issues)  
**Frågor?** Se [STATSBIDRAG_PILOT.md](STATSBIDRAG_PILOT.md)

---

## 📄 Licens

MIT License - se [LICENSE](LICENSE) för detaljer

---

## 🌟 Tack till

- [Sentence Transformers](https://www.sbert.net/) - AI-modeller
- [FAISS](https://github.com/facebookresearch/faiss) - Vektorsökning
- [Grants.gov](https://grants.gov/) - Testdata

---

**Skapad:** November 2024  
**Status:** ✅ Fungerande proof-of-concept  
**Nästa steg:** Anpassa för svenska statsbidrag → Bygg webbgränssnitt → Lansera!
