def calcular_score_governança(registros, metas):
    # Contagem de lançamentos
    contagem = {prog: 0 for prog in metas.keys()}
    for reg in registros:
        p = reg.get("programa")
        if p in contagem:
            contagem[p] += 1

    score_total = 0
    detalhes_metas = []

    for prog, meta in metas.items():
        realizado = contagem[prog]
        meta_alvo = meta["meta_semanal"]
        peso = meta["peso"]
        
        # Percentual de atingimento limitado a 100% por item
        pct_item = min(100.0, (realizado / meta_alvo) * 100) if meta_alvo > 0 else 0
        ponderado = (pct_item * peso) / 100
        score_total += ponderado

        detalhes_metas.append({
            "programa": prog,
            "realizado": realizado,
            "meta": meta_alvo,
            "peso": peso,
            "pct": round(pct_item, 1)
        })

    return round(score_total, 1), detalhes_metas