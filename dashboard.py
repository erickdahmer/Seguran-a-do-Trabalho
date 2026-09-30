import json
from datetime import datetime

def carregar_dados_iniciais():
    # Lista de Colaboradores Cadastrados
    colaboradores = [
        {"id": "COL-001", "nome": "Raquel Carvalho", "funcao": "TST", "empresa": "JB DIAS"},
        {"id": "COL-002", "nome": "Josinei Buchor", "funcao": "Líder Operacional", "empresa": "JB DIAS"},
        {"id": "COL-003", "nome": "Carlos Silva", "funcao": "Operador", "empresa": "JB DIAS"},
        {"id": "COL-004", "nome": "Mariana Souza", "funcao": "Supervisora EHS", "empresa": "JB DIAS"},
        {"id": "COL-005", "nome": "João Pedro", "funcao": "Mecânico", "empresa": "JB DIAS"}
    ]

    # Registros Iniciais
    registros = [
        {
            "id": "REG-001",
            "data": "2026-08-21",
            "programa": "IPS",
            "empresa": "JB DIAS",
            "responsavel": "Raquel Carvalho",
            "funcao": "TST",
            "lider": "Josinei Buchor",
            "colaborador_envolvido": "Carlos Silva",
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
            "colaborador_envolvido": "João Pedro",
            "houve_desvio": "Sim",
            "qtd_pessoas": 2,
            "descricao": "Trabalho em altura sem ancoragem dupla na estrutura",
            "status": "Em Tratativa (QA)"
        }
    ]
    
    # Metas CMPC
    metas_cmpc = {
        "CUIDAR": {"meta_semanal": 4, "peso": 30},
        "IPS": {"meta_semanal": 2, "peso": 10},
        "Relatório de Inspeção": {"meta_semanal": 2, "peso": 30},
        "DDS": {"meta_semanal": 1, "peso": 5},
        "Auditoria PT/AST": {"meta_semanal": 2, "peso": 5},
        "Reunião Semanal": {"meta_semanal": 1, "peso": 10},
        "Estatística HHT": {"meta_semanal": 1, "peso": 10}
    }
    
    return registros, metas_cmpc, colaboradores