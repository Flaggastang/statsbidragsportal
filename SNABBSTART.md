# 🚀 Snabbstart - Grants.gov Demo

## Tre enkla steg:

### 1️⃣ Installera
```bash
pip install -r requirements.txt
```
*Tar 2-5 minuter första gången*

### 2️⃣ Indexera
```bash
python scripts/fetch_and_index_grants.py
```
*Hämtar bidrag och bygger sökindex (2-3 minuter)*

### 3️⃣ Kör demon
```bash
python demo_grants.py
```
*Välj läge 1 för att se förberedda exempel!*

---

## 🎯 Vad du får:

✅ Ett fungerande AI-söksystem för bidrag  
✅ ~200 riktiga bidrag från Grants.gov  
✅ Semantisk sökning (förstår betydelse, inte bara ord)  
✅ Redo att anpassas för svenska statsbidrag  

---

## 📝 Test-frågor (interaktivt läge):

- "funding for education programs helping disadvantaged youth"
- "environmental protection climate change"
- "community health wellness programs"

---

## 🔄 Anpassa för svenska statsbidrag:

1. Ersätt API-anrop i `scripts/fetch_and_index_grants.py`
2. Anpassa datafält till er struktur
3. Byt till flerspråkig modell för bättre svenskstöd
4. Kör indexering med er data
5. Klart! 🎉

Se **GRANTS_DEMO_README.md** för detaljer.

