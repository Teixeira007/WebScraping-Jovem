"""
Script de teste para analisar a API da Guanabara
Objetivo: Verificar a resposta da API e entender a estrutura dos dados
"""

import requests
import json
from datetime import datetime

def test_guanabara_api():
    """Testa a requisição da API Guanabara"""
    
    url = "https://arara-core-proxy.gipsyy.com.br/app/sale/trips"
    
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiIzN2EyOTRmZS0zZjFiLTRhZjEtYjdjOS01NjM4ZDY2ZDEzMzkiLCJ1bmlxdWVfbmFtZSI6IklOVEVSIiwiSWRVc2VyIjoiMjUxNCIsIlRlbmFudCI6InNtYXJ0YnVzLWdhdGV3YXkiLCJDb21wYW5pZXMiOiIxfHIsMnxyLDN8ciw1fHIsNnxyLDR8ciwxMHxyLDEzfHIsMTF8ciwxNXx3LDE0fHciLCJuYmYiOjE3NjkwMDQyNzQsImV4cCI6MTgwMDU0MDI3NCwiaWF0IjoxNzY5MDA0Mjc0fQ.H1wHvKB0WZNoJmyrVeWcGy-yYKk3FTN1mGscBlTo4WQ",
        "content-type": "application/json",
        "identifierworkstation": "306C3125-CF50-40BA-AB8B-C2C2736E1629",
        "iduser": "2514",
        "origin": "https://www.viajeguanabara.com.br",
        "productid": "487a774c-0485-401f-84d2-61ed508becc3",
        "referer": "https://www.viajeguanabara.com.br/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
    }
    
    payload = {
        "departureLocationName": "Joao Pessoa - PB",
        "arrivalLocationName": "Irece - BA",
        "isReturn": False,
        "departureDate": "2026-02-17T00:00:00.000Z",
        "seats": "1",
        "idBookingCouponRevalidation": None,
        "searchType": 2,
        "discountType": None,
        "isOpen": False,
        "passengers": [
            {
                "idPassengerClassification": 13,
                "quantity": 1
            }
        ]
    }
    
    print("=" * 60)
    print("TESTE DA API GUANABARA")
    print("=" * 60)
    print(f"\nURL: {url}")
    print(f"Data da consulta: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nRota: {payload['departureLocationName']} → {payload['arrivalLocationName']}")
    print(f"Data da viagem: {payload['departureDate']}")
    print(f"Passageiros: {payload['passengers']}")
    print("\n" + "-" * 60)
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("\n✅ Requisição bem-sucedida!")
            data = response.json()
            
            # Salvar resposta completa
            with open("api_response_full.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print("\n📄 Resposta completa salva em: api_response_full.json")
            
            # Análise da estrutura
            print("\n" + "=" * 60)
            print("ANÁLISE DA ESTRUTURA DA RESPOSTA")
            print("=" * 60)
            print(f"\nTipo de dados: {type(data)}")
            
            if isinstance(data, dict):
                print(f"Chaves principais: {list(data.keys())}")
                
                # Exibir resumo de cada chave
                for key, value in data.items():
                    print(f"\n  • {key}:")
                    print(f"    - Tipo: {type(value)}")
                    if isinstance(value, list):
                        print(f"    - Quantidade de itens: {len(value)}")
                        if len(value) > 0:
                            print(f"    - Exemplo do primeiro item: {value[0]}")
                    elif isinstance(value, dict):
                        print(f"    - Chaves: {list(value.keys())}")
                    else:
                        print(f"    - Valor: {value}")
            
            elif isinstance(data, list):
                print(f"Quantidade de itens na lista: {len(data)}")
                if len(data) > 0:
                    print(f"Estrutura do primeiro item: {json.dumps(data[0], indent=2, ensure_ascii=False)}")
            
        else:
            print(f"\n❌ Erro na requisição!")
            print(f"Resposta: {response.text}")
            
    except requests.exceptions.Timeout:
        print("\n⏱️ Timeout na requisição!")
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Erro na requisição: {e}")
    except json.JSONDecodeError as e:
        print(f"\n❌ Erro ao decodificar JSON: {e}")
        print(f"Resposta bruta: {response.text}")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_guanabara_api()
