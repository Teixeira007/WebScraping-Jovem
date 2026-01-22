"""
Script para analisar campos price e originalPrice na resposta da API
"""

import json

# Carregar resposta da API
with open("api_response_full.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("=" * 80)
print("ANÁLISE DE PREÇOS E DESCONTOS - API GUANABARA")
print("=" * 80)

# Analisar trips
if "trips" in data:
    trips = data["trips"]
    print(f"\nTotal de viagens encontradas: {len(trips)}")
    
    for i, trip in enumerate(trips):
        print(f"\n{'=' * 40}")
        print(f"VIAGEM #{i+1}")
        print(f"{'=' * 40}")
        
        # Informações básicas
        print(f"Origem: {trip.get('departureLocationName')}")
        print(f"Destino: {trip.get('arrivalLocationName')}")
        print(f"Data/Hora Partida: {trip.get('departureDateTime')}")
        print(f"Classe: {trip.get('classOfServiceName')}")
        print(f"Assentos Disponíveis: {trip.get('availableSeats')}")
        
        # Análise de preços
        price = trip.get('price')
        original_price = trip.get('originalPrice')
        
        print(f"\n  💰 PREÇOS:")
        print(f"  - Preço atual: R$ {price}")
        print(f"  - Preço original: R$ {original_price}")
        
        if price and original_price:
            desconto = ((original_price - price) / original_price) * 100
            print(f"  - Desconto: {desconto:.1f}%")
            
            # Identificar tipo de benefício
            if desconto >= 45 and desconto <= 55:
                print(f"  - ✅ POSSÍVEL ID JOVEM 50%")
            elif desconto >= 95:
                print(f"  - ✅ POSSÍVEL ID JOVEM 100%")
            elif desconto > 0:
                print(f"  - ℹ️  DESCONTO DE {desconto:.1f}% (verificar tipo)")

print("\n" + "=" * 80)
