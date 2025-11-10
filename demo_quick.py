"""
GRANTS.GOV DEMO - Snabbversion
==============================
Visar alla resultat direkt utan pauser
"""

from scripts.query_grants import query_grants

# Demo-frågor
demo_queries = [
    {
        "scenario": "🎓 Utbildning & ungdom",
        "query": "funding for education programs helping disadvantaged youth",
        "description": "En kommun söker bidrag för att hjälpa unga i utsatta områden"
    },
    {
        "scenario": "🌍 Miljö & hållbarhet",
        "query": "environmental protection climate change sustainability",
        "description": "En kommun vill arbeta med klimatfrågor och miljöskydd"
    },
    {
        "scenario": "🏥 Folkhälsa",
        "query": "community health wellness programs mental health",
        "description": "En kommun vill satsa på folkhälsa och psykisk hälsa"
    },
    {
        "scenario": "🤝 Integration & samhällsutveckling",
        "query": "community development social services integration",
        "description": "En kommun söker stöd för integrationsarbete"
    }
]

print("\n" + "="*80)
print("🎯 GRANTS.GOV DEMO - INTELLIGENT BIDRAGSSÖKNING")
print("="*80)
print("\nDetta system använder AI för att förstå din fråga och hitta")
print("relevanta bidrag baserat på BETYDELSE, inte bara nyckelord.\n")
print("="*80)

for i, demo in enumerate(demo_queries, 1):
    print(f"\n{'═'*80}")
    print(f"SCENARIO {i}: {demo['scenario']}")
    print(f"{'═'*80}")
    print(f"📝 Situation: {demo['description']}")
    print(f"❓ Fråga: '{demo['query']}'")
    
    results = query_grants(demo['query'], k=3, verbose=False)
    
    if results:
        print(f"\n✅ Top 3 matchningar:\n")
        for j, grant in enumerate(results, 1):
            print(f"{j}. {grant['title']}")
            print(f"   🏛️  {grant['agency']}")
            print(f"   📅 Deadline: {grant['deadline']}")
            
            # Visa kort beskrivning
            desc = grant['description']
            if len(desc) > 150:
                desc = desc[:150] + "..."
            print(f"   📝 {desc}")
            print()

print("\n" + "="*80)
print("✅ DEMO SLUTFÖRD!")
print("="*80)
print("\n💡 Fördelar med AI-sökning:")
print("  ✓ Förstår BETYDELSE, inte bara nyckelord")
print("  ✓ Hittar relevanta bidrag även med olika formuleringar")
print("  ✓ Fungerar på svenska OCH engelska (med flerspråkig modell)")
print("  ✓ Snabb sökning bland hundratals bidrag")
print("\n🎯 Nästa steg:")
print("  1. Samla era 160 svenska statsbidrag")
print("  2. Anpassa fetch_and_index_grants.py för er datakälla")
print("  3. Bygg webbgränssnitt")
print("  4. Lägg till filter och avancerade funktioner")
print("\n✨ Systemet är redo att anpassas för svenska statsbidrag!")
print("="*80 + "\n")

