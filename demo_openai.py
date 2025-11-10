"""
STATSBIDRAGSPORTAL MED OPENAI GPT - INTELLIGENT KONVERSATION
============================================================

Detta script lägger till en intelligent konversationsassistent ovanpå
den befintliga sökmotorn. GPT hjälper användaren att:
- Formulera bättre sökfrågor
- Förstå vilka bidrag som passar bäst
- Ställa följdfrågor
- Få rekommendationer

Teknisk stack:
- Sökning: FAISS (snabb, lokal) [befintlig]
- Konversation: OpenAI GPT-4 (intelligent dialog) [nytt!]
"""

import os
from scripts.query_grants import query_grants
import json

# Kräver OpenAI API-nyckel
try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except ImportError:
    print("❌ OpenAI-biblioteket saknas. Installera med: pip install openai")
    exit(1)
except Exception as e:
    print("❌ Fel vid initiering av OpenAI. Kontrollera att OPENAI_API_KEY är satt.")
    print(f"   Sätt med: export OPENAI_API_KEY='din-api-nyckel'")
    exit(1)

# GPT-systemmeddelande (definierar assistentens roll)
SYSTEM_PROMPT = """Du är en hjälpsam assistent för svenska kommuner som söker statsbidrag.

Din uppgift:
1. Hjälpa användaren formulera vad de söker
2. Analysera sökresultat och förklara vilka som passar bäst
3. Ställa uppföljningsfrågor för att förstå behoven bättre
4. Ge konkreta rekommendationer

Du har tillgång till en sökmotor som hittar relevanta bidrag baserat på semantisk matchning.

Kommunicera på svenska och var professionell men tillgänglig.
"""

def search_with_gpt(user_message, conversation_history=None):
    """
    Använder GPT för att förstå användarens behov och ge intelligenta svar
    """
    if conversation_history is None:
        conversation_history = []
    
    # Lägg till användarmeddelande
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    # GPT analyserar frågan först
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ] + conversation_history
    
    print("\n🤖 Tänker...")
    
    # Första GPT-anrop: Förstå vad användaren vill ha
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Snabb och kostnadseffektiv
        messages=messages + [{
            "role": "system",
            "content": """Baserat på användarens meddelande, formulera EN KORT sökfråga på engelska 
            som kan användas för att söka i bidragsdatabasen. Svara ENDAST med sökfrågan, inget annat.
            
            Exempel:
            Användare: "Vi behöver pengar för att bygga cykelvägar"
            Du: "infrastructure cycling transportation community development"
            
            Användare: "Har ni något för integration?"
            Du: "integration immigrant settlement social services"
            """
        }],
        temperature=0.3,
        max_tokens=100
    )
    
    search_query = response.choices[0].message.content.strip()
    print(f"🔍 Söker efter: '{search_query}'")
    
    # Sök i databasen
    results = query_grants(search_query, k=5, verbose=False)
    
    # Formatera resultat för GPT
    results_text = "\n\n".join([
        f"Bidrag {i+1}:\n"
        f"Titel: {r['title']}\n"
        f"Myndighet: {r['agency']}\n"
        f"Deadline: {r['deadline']}\n"
        f"Kategori: {r['category']}\n"
        f"Beskrivning: {r['description'][:200]}..."
        for i, r in enumerate(results)
    ])
    
    # GPT analyserar resultaten och svarar användaren
    conversation_history.append({
        "role": "assistant",
        "content": f"[INTERN SÖKNING: '{search_query}']"
    })
    
    final_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages + [
            {
                "role": "system",
                "content": f"""Här är sökresultaten från bidragsdatabasen:

{results_text}

Analysera dessa resultat och:
1. Sammanfatta kort vilka bidrag som hittades
2. Rekommendera de 1-3 mest relevanta
3. Förklara VARFÖR de passar användarens behov
4. Fråga om användaren vill veta mer eller söka annorlunda

Var KONKRET och använd bidragstitlar när du refererar till dem.
Svara på SVENSKA.
"""
            }
        ],
        temperature=0.7,
        max_tokens=800
    )
    
    assistant_message = final_response.choices[0].message.content
    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })
    
    return assistant_message, results, conversation_history

def interactive_chat():
    """
    Interaktiv chatt med GPT-assistent
    """
    print("\n" + "="*80)
    print("🤖 INTELLIGENT BIDRAGSSÖKNING MED GPT")
    print("="*80)
    print("\nHej! Jag är din AI-assistent för statsbidrag.")
    print("Berätta vad din kommun behöver så hjälper jag dig hitta rätt bidrag.")
    print("\nSkriv 'exit' för att avsluta.\n")
    print("="*80)
    
    conversation_history = []
    
    while True:
        try:
            # Få användarinput
            user_input = input("\n💬 Du: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit', 'avsluta', 'q']:
                print("\n👋 Tack för att du använde bidragsassistenten!")
                print("Lycka till med er ansökan!")
                break
            
            # Sök med GPT
            response, results, conversation_history = search_with_gpt(
                user_input, 
                conversation_history
            )
            
            # Visa svar
            print(f"\n🤖 Assistent:\n{response}")
            
            # Visa länkar (diskret)
            if results:
                print("\n" + "─"*80)
                print("📎 Länkar till bidragen:")
                for i, r in enumerate(results[:3], 1):
                    print(f"{i}. {r['title'][:60]}...")
                    print(f"   🔗 {r['url']}")
        
        except KeyboardInterrupt:
            print("\n\n👋 Tack för att du använde bidragsassistenten!")
            break
        except Exception as e:
            print(f"\n❌ Ett fel uppstod: {str(e)}")
            print("Försök igen eller skriv 'exit' för att avsluta.")

def demo_scenarios():
    """
    Kör förberedda demo-scenarion med GPT
    """
    print("\n" + "="*80)
    print("🎯 GPT DEMO - INTELLIGENTA KONVERSATIONER")
    print("="*80)
    
    scenarios = [
        {
            "title": "Innovation & teknologi",
            "message": "Vi är en mindre kommun som vill satsa på innovation och digitalisering. Finns det något för oss?"
        },
        {
            "title": "Ungas psykiska hälsa",
            "message": "Vi ser ökande behov av insatser för ungas psykiska hälsa. Vad finns?"
        },
        {
            "title": "Hållbar stadsutveckling",
            "message": "Vi planerar att göra vårt centrum mer gång- och cykelvänligt och hållbart. Finns det stöd för det?"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'═'*80}")
        print(f"SCENARIO {i}: {scenario['title']}")
        print(f"{'═'*80}")
        print(f"\n💬 Kommun: \"{scenario['message']}\"")
        
        response, results, _ = search_with_gpt(scenario['message'])
        
        print(f"\n🤖 GPT-assistent:\n{response}")
        
        if i < len(scenarios):
            input("\n[Tryck ENTER för nästa scenario...]")
    
    print("\n" + "="*80)
    print("✅ DEMO SLUTFÖRD!")
    print("="*80)
    print("\n💡 Fördelar med GPT-integration:")
    print("  ✓ Förstår naturligt språk och kontext")
    print("  ✓ Ger personliga rekommendationer")
    print("  ✓ Kan ställa uppföljningsfrågor")
    print("  ✓ Förklarar VARFÖR bidrag passar")
    print("  ✓ Konversationell upplevelse")
    print("\n🎯 Kombinerar det bästa av båda världar:")
    print("  • Snabb FAISS-sökning (lokal, gratis)")
    print("  • Intelligent GPT-analys (smart, hjälpsam)")

if __name__ == "__main__":
    import sys
    
    # Kontrollera API-nyckel
    if not os.getenv("OPENAI_API_KEY"):
        print("\n" + "="*80)
        print("⚠️  OPENAI_API_KEY SAKNAS")
        print("="*80)
        print("\nFör att använda denna demo behöver du en OpenAI API-nyckel.")
        print("\nSteg 1: Få en API-nyckel från https://platform.openai.com/api-keys")
        print("Steg 2: Sätt environment-variabeln:")
        print("\n  Windows (PowerShell):")
        print('  $env:OPENAI_API_KEY="sk-..."')
        print("\n  Mac/Linux:")
        print('  export OPENAI_API_KEY="sk-..."')
        print("\nSteg 3: Kör scriptet igen")
        print("="*80)
        sys.exit(1)
    
    # Välj läge
    print("\n🎯 Välj läge:")
    print("1. Demo med förberedda scenarion")
    print("2. Interaktiv chatt")
    
    choice = input("\nVälj (1 eller 2): ").strip()
    
    if choice == "1":
        demo_scenarios()
    elif choice == "2":
        interactive_chat()
    else:
        print("Ogiltigt val. Kör programmet igen.")

