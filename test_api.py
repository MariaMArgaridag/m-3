#!/usr/bin/env python
"""
Script de teste da API Cybersecurity Threats
Testa todos os endpoints principais
"""

import requests
import json
import time

# Configuração
BASE_URL = "http://127.0.0.1:8000"
HEADERS = {"Content-Type": "application/json"}

# Cores para output no terminal
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

def test_endpoint(method, path, data=None, expected_status=200):
    """Testa um endpoint e retorna o resultado"""
    url = f"{BASE_URL}{path}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=HEADERS)
        elif method == "POST":
            response = requests.post(url, json=data, headers=HEADERS)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=HEADERS)
        elif method == "DELETE":
            response = requests.delete(url, headers=HEADERS)
        
        success = response.status_code == expected_status
        status_text = f"{GREEN}✓{RESET}" if success else f"{RED}✗{RESET}"
        
        print(f"{status_text} {method:6} {path:50} -> {response.status_code}")
        
        if not success and response.text:
            print(f"   {RED}Resposta: {response.text[:100]}{RESET}")
        
        return response
        
    except requests.exceptions.ConnectionError:
        print(f"{RED}✗ Conexão recusada. Certifique-se que o servidor está rodando!{RESET}")
        print(f"   {BLUE}Execute: python run.py{RESET}")
        return None
    except Exception as e:
        print(f"{RED}✗ Erro: {str(e)}{RESET}")
        return None


def main():
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}🧪 TESTES DA API CYBERSECURITY THREATS{RESET}")
    print(f"{BLUE}{'='*80}{RESET}\n")
    
    # Teste 1: Health Check
    print(f"{BLUE}[1] Health Check{RESET}")
    test_endpoint("GET", "/health", expected_status=200)
    
    # Teste 2: Listar Attack Types
    print(f"\n{BLUE}[2] Attack Types - Listar{RESET}")
    response = test_endpoint("GET", "/attacks", expected_status=200)
    if response and response.status_code == 200:
        data = response.json()
        print(f"   📊 Total de ataques: {len(data)}")
        if data:
            print(f"   📌 Exemplo: {data[0]['type']} (ID: {data[0]['id']})")
    
    # Teste 3: Listar Defense Mechanisms
    print(f"\n{BLUE}[3] Defense Mechanisms - Listar{RESET}")
    response = test_endpoint("GET", "/defenses", expected_status=200)
    if response and response.status_code == 200:
        data = response.json()
        print(f"   📊 Total de defesas: {len(data)}")
        if data:
            print(f"   📌 Exemplo: {data[0]['mechanism']} (ID: {data[0]['id']})")
    
    # Teste 4: Listar Vulnerabilities
    print(f"\n{BLUE}[4] Vulnerabilities - Listar{RESET}")
    response = test_endpoint("GET", "/vulnerabilities", expected_status=200)
    if response and response.status_code == 200:
        data = response.json()
        print(f"   📊 Total de vulnerabilidades: {len(data)}")
    
    # Teste 5: Listar Incidents
    print(f"\n{BLUE}[5] Incidents - Listar{RESET}")
    response = test_endpoint("GET", "/incidents", expected_status=200)
    if response and response.status_code == 200:
        data = response.json()
        print(f"   📊 Total de incidentes: {len(data)}")
        if data:
            print(f"   📌 Exemplo: {data[0]['country']} ({data[0]['year']}) - Perda: ${data[0]['financial_loss_million']}M")
    
    # Teste 6: Filtrar Incidents por país
    print(f"\n{BLUE}[6] Incidents - Filtrar por país (Brasil){RESET}")
    response = test_endpoint("GET", "/incidents?country=Brazil", expected_status=200)
    if response and response.status_code == 200:
        data = response.json()
        print(f"   📊 Incidentes no Brasil: {len(data)}")
    
    # Teste 7: Filtrar Incidents por ano
    print(f"\n{BLUE}[7] Incidents - Filtrar por ano (2023){RESET}")
    response = test_endpoint("GET", "/incidents?year=2023", expected_status=200)
    if response and response.status_code == 200:
        data = response.json()
        print(f"   📊 Incidentes em 2023: {len(data)}")
    
    # Teste 8: Statisticas
    print(f"\n{BLUE}[8] Estatísticas - Incidentes{RESET}")
    response = test_endpoint("GET", "/incidents/stats/all", expected_status=200)
    if response and response.status_code == 200:
        data = response.json()
        print(f"   💰 Perda financeira total: ${data['total_financial_loss_million']:.2f}M")
        print(f"   👥 Usuários afetados: {data['total_affected_users']}")
        print(f"   ⏱️  Tempo médio de resolução: {data['average_resolution_time_hours']:.1f}h")
    
    # Teste 9: Criar novo ataque (POST)
    print(f"\n{BLUE}[9] Attack Types - Criar novo{RESET}")
    new_attack = {"type": "Zero-Day Exploit"}
    response = test_endpoint("POST", "/attacks", data=new_attack, expected_status=201)
    if response and response.status_code == 201:
        attack_id = response.json()['id']
        print(f"   ✨ Novo ataque criado com ID: {attack_id}")
        
        # Teste 10: Obter o ataque criado
        print(f"\n{BLUE}[10] Attack Types - Obter por ID ({attack_id}){RESET}")
        test_endpoint("GET", f"/attacks/{attack_id}", expected_status=200)
        
        # Teste 11: Atualizar o ataque
        print(f"\n{BLUE}[11] Attack Types - Atualizar ID {attack_id}{RESET}")
        updated_attack = {"type": "Advanced Zero-Day"}
        test_endpoint("PUT", f"/attacks/{attack_id}", data=updated_attack, expected_status=200)
        
        # Teste 12: Deletar o ataque
        print(f"\n{BLUE}[12] Attack Types - Deletar ID {attack_id}{RESET}")
        test_endpoint("DELETE", f"/attacks/{attack_id}", expected_status=200)
    
    # Resumo
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{GREEN}✓ Testes concluídos!{RESET}")
    print(f"\n{BLUE}📚 Documentação interativa:{RESET}")
    print(f"   🔗 Swagger UI: http://127.0.0.1:8000/docs")
    print(f"   🔗 ReDoc: http://127.0.0.1:8000/redoc")
    print(f"\n{BLUE}{'='*80}{RESET}\n")


if __name__ == "__main__":
    main()
