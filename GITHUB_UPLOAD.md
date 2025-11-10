# 📤 Guide: Ladda upp till GitHub

Denna guide hjälper dig att ladda upp statsbidragspiloten till GitHub-repositoryt.

---

## 🗂️ Filer som ska laddas upp

### ✅ Källkod (nödvändiga filer)

```
statsbidragsportal/
├── scripts/
│   ├── __init__.py                    ✅ Python-modul
│   ├── fetch_and_index_grants.py      ✅ Indexeringsskript
│   ├── query_grants.py                ✅ Sökmotorn
│   └── utils.py                       ✅ Hjälpfunktioner
├── demo_grants.py                     ✅ Interaktiv demo
├── demo_quick.py                      ✅ Snabb demo
├── requirements.txt                   ✅ Python-beroenden
├── README.md                          ✅ GitHub README
├── STATSBIDRAG_PILOT.md              ✅ Detaljerad översikt
├── GRANTS_DEMO_README.md             ✅ Teknisk dokumentation
├── SNABBSTART.md                      ✅ Snabbguide
├── .gitignore                         ✅ Git-konfiguration
├── LICENSE                            ✅ MIT License
└── GITHUB_UPLOAD.md                   ✅ Denna guide
```

### ❌ Filer som INTE ska laddas upp

Dessa filer ignoreras automatiskt av `.gitignore`:

```
❌ data/                        # Genereras lokalt
   ├── grants_index.faiss       # FAISS-index
   ├── grants_data.json         # Bidragsdata
   ├── grants_metadata.txt      # Metadata
   ├── kpi_index.faiss          # Gammalt KPI-index
   └── kpi_ids.txt              # Gamla KPI-id

❌ artiklar/                    # Gamla projektfiler
❌ *.log                        # Loggfiler
❌ *.xlsx                       # Excel-filer
❌ __pycache__/                 # Python cache
❌ main.py                      # Gammalt KPI-script
❌ *_articles.json              # Gamla artikeldata
```

---

## 🚀 Steg-för-steg uppladdning

### Steg 1: Förbered repositoryt lokalt

```bash
# Navigera till projektmappen
cd "C:\PROJEKT VS code\kolada-kpi-matcher"

# Verifiera att .gitignore är korrekt
cat .gitignore

# Kontrollera vilka filer som kommer laddas upp
git status
```

### Steg 2: Initiera Git (om inte redan gjort)

```bash
# Initiera git repository
git init

# Lägg till remote (ditt GitHub-repo)
git remote add origin https://github.com/Flaggastang/statsbidragsportal.git

# Verifiera remote
git remote -v
```

### Steg 3: Lägg till filer

```bash
# Lägg till alla relevanta filer (respekterar .gitignore)
git add .

# Kontrollera vad som ska committas
git status

# Om du ser oönskade filer, ta bort dem:
# git reset HEAD <fil>
```

### Steg 4: Commit

```bash
git commit -m "Initial commit: Statsbidragssökning pilot med AI

- Fungerande proof-of-concept för AI-driven bidragssökning
- Hämtar data från Grants.gov API
- Semantisk sökning med FAISS och Sentence Transformers
- Inkluderar 3 demo-lägen
- Komplett dokumentation på svenska
- Redo att anpassas för svenska statsbidrag"
```

### Steg 5: Pusha till GitHub

```bash
# Om repositoryt är nytt och tomt
git branch -M main
git push -u origin main

# Om repositoryt redan har innehåll
git pull origin main --allow-unrelated-histories
git push origin main
```

---

## 🔧 Alternativ: Använd GitHub Desktop

Om du föredrar ett grafiskt gränssnitt:

1. Öppna GitHub Desktop
2. Välj **File → Add Local Repository**
3. Navigera till `C:\PROJEKT VS code\kolada-kpi-matcher`
4. Välj de filer du vill committa (respekterar .gitignore)
5. Skriv commit-meddelande
6. Klicka **Commit to main**
7. Klicka **Push origin**

---

## ✅ Verifiera uppladdningen

1. Gå till https://github.com/Flaggastang/statsbidragsportal
2. Kontrollera att följande finns:
   - ✅ README.md visas som startsida
   - ✅ scripts/ mapp med 4 filer
   - ✅ 3 demo-filer (demo_grants.py, demo_quick.py)
   - ✅ requirements.txt
   - ✅ Dokumentation (STATSBIDRAG_PILOT.md, etc.)
   - ❌ INGA .log filer
   - ❌ INGEN data/ mapp
   - ❌ INGA artiklar

3. Testa att andra kan klona:
   ```bash
   # I en annan mapp
   git clone https://github.com/Flaggastang/statsbidragsportal.git
   cd statsbidragsportal
   pip install -r requirements.txt
   python scripts/fetch_and_index_grants.py
   python demo_quick.py
   ```

---

## 📝 Efter uppladdning

### Lägg till GitHub Badges (valfritt)

Redigera README.md och lägg till:

```markdown
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-proof--of--concept-yellow.svg)]()
```

### Skapa GitHub Pages (valfritt)

1. Gå till **Settings → Pages**
2. Välj **Source: Deploy from a branch**
3. Välj **Branch: main**, **/ (root)**
4. Spara

README.md kommer att visas som en fin webbsida!

### Aktivera Issues

1. Gå till **Settings → Features**
2. Se till att **Issues** är aktiverat
3. Nu kan andra rapportera buggar och ge feedback

### Lägg till Topics (taggar)

1. Klicka på kugghjulet bredvid "About" på startsidan
2. Lägg till topics:
   - `ai`
   - `semantic-search`
   - `faiss`
   - `python`
   - `grants`
   - `statsbidrag`
   - `sverige`
   - `machine-learning`
   - `nlp`

---

## 🐛 Felsökning

### Problem: "fatal: remote origin already exists"

**Lösning:**
```bash
git remote remove origin
git remote add origin https://github.com/Flaggastang/statsbidragsportal.git
```

### Problem: "Updates were rejected because the remote contains work"

**Lösning:**
```bash
git pull origin main --allow-unrelated-histories
git push origin main
```

### Problem: Oönskade filer inkluderade

**Lösning:**
```bash
# Ta bort fil från staging
git reset HEAD <fil>

# Eller ta bort från både staging och Git-historik
git rm --cached <fil>

# Lägg till i .gitignore
echo "<fil>" >> .gitignore
```

### Problem: Stora filer (>100MB)

GitHub tillåter inte filer >100MB. Använd `.gitignore` för att exkludera dem.

```bash
# Kontrollera filstorlekar
find . -type f -size +10M -ls
```

---

## 📊 Projektstruktur efter uppladdning

```
GitHub Repository (publikt)
│
├── README.md                      ← Startsida, snabb introduktion
├── STATSBIDRAG_PILOT.md          ← Komplett guide och jämförelse
├── GRANTS_DEMO_README.md         ← Teknisk dokumentation
├── SNABBSTART.md                  ← Snabbguide för nybörjare
│
├── scripts/                       ← Källkod
│   ├── fetch_and_index_grants.py  ← Hämta och indexera
│   ├── query_grants.py            ← Sökmotorn
│   └── utils.py                   ← Hjälpfunktioner
│
├── demo_grants.py                 ← Interaktiv demo
├── demo_quick.py                  ← Snabb demo
│
├── requirements.txt               ← Python-paket
├── .gitignore                     ← Git-konfiguration
├── LICENSE                        ← MIT License
└── GITHUB_UPLOAD.md              ← Denna guide

Lokalt (genereras av användaren)
│
└── data/                          ← Skapas när man kör scripten
    ├── grants_index.faiss         ← FAISS-index
    ├── grants_data.json           ← Bidragsdata
    └── grants_metadata.txt        ← Metadata
```

---

## ✨ Nästa steg

När repositoryt är uppladdat:

1. ✅ Dela länken med teamet
2. ✅ Be andra testa installationen
3. ✅ Samla feedback via GitHub Issues
4. ✅ Planera nästa iteration
5. ✅ Dokumentera erfarenheter

---

**Lycka till med uppladdningen!** 🚀

Om du stöter på problem, öppna ett Issue på GitHub eller kontakta projektansvarig.

