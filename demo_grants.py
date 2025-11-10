"""
GRANTS.GOV DEMO - Intelligent Bidragssökning
=============================================

Detta är en demo som visar hur AI-driven semantisk sökning kan användas
för att hjälpa kommuner hitta relevanta statsbidrag.

Demo använder Grants.gov API för att visa konceptet.

Användning:
-----------
1. Kör först indexering (engångskörning):
   python scripts/fetch_and_index_grants.py

2. Kör sedan detta demoscript:
   python demo_grants.py

Eller använd de förberedda demo-frågorna nedan.
"""

from scripts.query_grants import query_grants, display_results

def run_demo():
    print("\n" + "="*80)
    print("🎯 GRANTS.GOV DEMO - INTELLIGENT BIDRAGSSÖKNING")
    print("="*80)
    print("\nDetta system använder AI för att förstå din fråga och hitta")
    print("relevanta bidrag baserat på BETYDELSE, inte bara nyckelord.\n")
    
    # Demo-frågor med olika scenarion
    demo_queries = [
        {
            "scenario": "Utbildning & ungdom",
            "query": "funding for education programs helping disadvantaged youth",
            "description": "En kommun söker bidrag för att hjälpa unga i utsatta områden"
        },
        {
            "scenario": "Miljö & hållbarhet",
            "query": "environmental protection climate change sustainability",
            "description": "En kommun vill arbeta med klimatfrågor och miljöskydd"
        },
        {
            "scenario": "Folkhälsa",
            "query": "community health wellness programs mental health",
            "description": "En kommun vill satsa på folkhälsa och psykisk hälsa"
        },
        {
            "scenario": "Integration & samhällsutveckling",
            "query": "community development social services integration",
            "description": "En kommun söker stöd för integrationsarbete"
        }
    ]
    
    print("DEMO-LÄGEN:")
    print("1. Kör förberedda demo-frågor")
    print("2. Sök själv (interaktivt läge)")
    print()
    
    choice = input("Välj läge (1 eller 2): ").strip()
    
    if choice == "1":
        # Kör demo-frågor
        print("\n" + "="*80)
        print("KÖRT DEMO MED FÖRBEREDDA SCENARION")
        print("="*80)
        
        for i, demo in enumerate(demo_queries, 1):
            print(f"\n{'═'*80}")
            print(f"SCENARIO {i}: {demo['scenario']}")
            print(f"{'═'*80}")
            print(f"🎯 Situation: {demo['description']}")
            print(f"❓ Fråga: '{demo['query']}'")
            
            results = query_grants(demo['query'], k=3, verbose=False)
            
            if results:
                print(f"\n✅ Top 3 matchningar:\n")
                for j, grant in enumerate(results, 1):
                    print(f"{j}. {grant['title']}")
                    print(f"   💰 {grant['agency']}")
                    print(f"   📅 Deadline: {grant['deadline']}")
                    print()
            
            if i < len(demo_queries):
                input("Tryck ENTER för nästa scenario...")
        
        print("\n" + "="*80)
        print("✅ DEMO SLUTFÖRD!")
        print("="*80)
        print("\nFördelar med AI-sökning:")
        print("  ✓ Förstår BETYDELSE, inte bara nyckelord")
        print("  ✓ Hittar relevanta bidrag även med olika formuleringar")
        print("  ✓ Fungerar på svenska OCH engelska (med svensk modell)")
        print("  ✓ Snabb sökning bland tusentals bidrag")
        print("\nNästa steg: Anpassa för svenska statsbidrag!")
        
    elif choice == "2":
        # Interaktivt läge
        print("\n" + "="*80)
        print("INTERAKTIVT LÄGE")
        print("="*80)
        print("\nBeskriv vad du söker bidrag för (på engelska för bäst resultat)")
        print("Skriv 'exit' för att avsluta\n")
        
        while True:
            try:
                query = input("🔍 Din fråga: ").strip()
                
                if not query:
                    continue
                
                if query.lower() in ['exit', 'quit', 'q', 'avsluta']:
                    print("\n👋 Tack för att du testade demon!")
                    break
                
                results = query_grants(query, k=5)
                display_results(query, results)
                
                print("\n")
            
            except KeyboardInterrupt:
                print("\n\n👋 Tack för att du testade demon!")
                break
    else:
        print("\n❌ Ogiltigt val. Kör programmet igen.")

if __name__ == "__main__":
    try:
        run_demo()
    except FileNotFoundError:
        print("\n" + "="*80)
        print("❌ FEL: Index-filer saknas")
        print("="*80)
        print("\nDu måste först köra indexeringen:")
        print("\n  python scripts/fetch_and_index_grants.py\n")
        print("Detta hämtar bidrag från Grants.gov och skapar sökindexet.")
        print("Det tar cirka 2-3 minuter första gången.")
        print("="*80)
    except Exception as e:
        print(f"\n❌ Ett oväntat fel uppstod: {str(e)}")
        import traceback
        traceback.print_exc()

