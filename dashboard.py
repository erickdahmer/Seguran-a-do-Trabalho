import json
from datetime import datetime

def carregar_dados_iniciais():
    # Registros Iniciais do IPS e Programas CMPC
    registros = [
        {
            "id": "REG-001",
            "data": "2026-08-21",
            "programa": "IPS",
            "empresa": "JB DIAS",
            "responsavel": "Raquel Carvalho",
            "funcao": "TST",
            "lider": "Josinei Buchor",
            "houve_desvio": "Sim",
            "qtd_pessoas": 1,
            "descricao": "Protetor auricular danificado na linha de montagem",
            "status": "Concluído"
        },
        {
            "id": "REG-002",
            "data": "2026-08-22",
            "programa": "CUIDAR",
            "empresa": "JB DIAS",
            "responsavel": "Raquel Carvalho",
            "funcao": "TST",
            "lider": "Josinei Buchor",
            "houve_desvio": "Sim",
            "qtd_pessoas": 2,
            "descricao": "Trabalho em altura sem ancoragem dupla na estrutura",
            "status": "Em Tratativa (QA)"
        },
        {
            "id": "REG-003",
            "data": "2026-08-24",
            "programa": "Auditoria PT/AST",
            "empresa": "JB DIAS",
            "responsavel": "Raquel Carvalho",
            "funcao": "TST",
            "lider": "Josinei Buchor",
            "houve_desvio": "Não",
            "qtd_pessoas": 0,
            "descricao": "Auditoria de rotina na PT de corte e solda OK",
            "status": "Concluído"
        }
    ]
    
    # Metas Obrigatórias CMPC para JB Dias
    metas_cmpc = {
        "CUIDAR": {"meta_semanal": 4, "peso": 30},
        "IPS": {"meta_semanal": 2, "peso": 10},
        "Relatório de Inspeção": {"meta_semanal": 2, "peso": 30},
        "DDS": {"meta_semanal": 1, "peso": 5},
        "Auditoria PT/AST": {"meta_semanal": 2, "peso": 5},
        "Reunião Semanal": {"meta_semanal": 1, "peso": 10},
        "Estatística HHT": {"meta_semanal": 1, "peso": 10}
    }
    
    return registros, metas_cmpc