import os
import json
import webbrowser
from dashboard import carregar_dados_iniciais
from analisador import calcular_score_governança

CAMINHO_SAIDA = os.path.join(os.path.dirname(__file__), "index.html")

def compilar_app():
    registros, metas = carregar_dados_iniciais()
    score, detalhes = calcular_score_governança(registros, metas)

    json_registros = json.dumps(registros, ensure_ascii=False)
    json_metas = json.dumps(metas, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JB DIAS | App EHS CMPC Command Center</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ background-color: #090d16; color: #cbd5e1; font-family: system-ui, -apple-system, sans-serif; }}
        .card {{ background-color: #111827; border: 1px solid #1e293b; border-radius: 0.75rem; }}
        .input-field {{ background-color: #1f2937; border: 1px solid #374151; color: #white; border-radius: 0.375rem; padding: 0.5rem; width: 100%; }}
    </style>
</head>
<body class="p-4 md:p-6">
    <div id="app" class="max-w-7xl mx-auto">
        <!-- HEADER GOVERNANÇA CMPC -->
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 border-b border-slate-800 pb-4 gap-4">
            <div>
                <div class="flex items-center gap-3">
                    <h1 class="text-2xl font-bold text-white tracking-wide">JB DIAS — Gestão de EHS</h1>
                    <span class="bg-emerald-900/80 text-emerald-300 border border-emerald-500/50 text-xs px-3 py-1 rounded-full font-semibold">
                        Contrato CMPC
                    </span>
                </div>
                <p class="text-sm text-slate-400 mt-1">Painel Interativo de Registros de Campo & Indicadores da Matriz CMPC</p>
            </div>
            
            <div class="flex items-center gap-4">
                <div class="card px-5 py-2.5 text-center border-emerald-500/40">
                    <span class="text-xs text-slate-400 uppercase font-semibold">Índice Compliance CMPC</span>
                    <div id="scoreDisplay" class="text-2xl font-black text-emerald-400">{score}%</div>
                </div>
                <button onclick="abrirModal()" class="bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-2.5 rounded-lg font-semibold text-sm transition flex items-center gap-2">
                    ➕ Novo Registro CMPC
                </button>
            </div>
        </div>

        <!-- CARDS DE METAS OBRIGATÓRIAS CMPC -->
        <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3 mb-6" id="cardsMetas"></div>

        <!-- DASHBOARD PRINCIPAL (INSPIRADO NO LAYOUT DA CMPC) -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
            <!-- Gráfico de Atingimento por Programa -->
            <div class="card p-5 lg:col-span-2">
                <h2 class="text-base font-semibold text-white mb-4 flex items-center justify-between">
                    <span>📊 Desempenho por Programa de Segurança (Meta Semanal)</span>
                    <span class="text-xs text-slate-400">Metas CMPC</span>
                </h2>
                <canvas id="chartMeta" height="110"></canvas>
            </div>

            <!-- Visão por TST / Líder -->
            <div class="card p-5">
                <h2 class="text-base font-semibold text-white mb-4">👤 Produção por Responsável</h2>
                <div class="space-y-4">
                    <div class="p-3 bg-slate-800/60 rounded-lg">
                        <span class="text-xs text-slate-400 uppercase font-bold">TST Responsável</span>
                        <div class="text-lg font-bold text-white">Raquel Carvalho - JB DIAS</div>
                        <div class="w-full bg-slate-700 h-2 rounded-full mt-2">
                            <div class="bg-emerald-500 h-2 rounded-full" style="width: 85%"></div>
                        </div>
                    </div>
                    <div class="p-3 bg-slate-800/60 rounded-lg">
                        <span class="text-xs text-slate-400 uppercase font-bold">Líder Operacional</span>
                        <div class="text-lg font-bold text-white">Josinei Buchor - JB DIAS</div>
                        <div class="w-full bg-slate-700 h-2 rounded-full mt-2">
                            <div class="bg-blue-500 h-2 rounded-full" style="width: 70%"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TABELA INTERATIVA DOS REGISTROS (DETALHES DO REGISTRO) -->
        <div class="card p-5">
            <div class="flex justify-between items-center mb-4">
                <h2 class="text-base font-semibold text-white">📋 Detalhes dos Registros de Campo (CMPC / IPS / CUIDAR)</h2>
                <span class="text-xs text-slate-400">Cadastre, edite ou remova registros para atualizar o score</span>
            </div>
            
            <div class="overflow-x-auto">
                <table class="w-full text-left text-sm text-slate-300">
                    <thead class="bg-slate-800/80 text-slate-400 uppercase text-xs">
                        <tr>
                            <th class="p-3">Data</th>
                            <th class="p-3">Programa</th>
                            <th class="p-3">TST / Líder</th>
                            <th class="p-3">Houve Desvio?</th>
                            <th class="p-3">Pessoas em Desvio</th>
                            <th class="p-3">Descrição do Desvio / Ação</th>
                            <th class="p-3 text-center">Ações</th>
                        </tr>
                    </thead>
                    <tbody id="tblRegistros" class="divide-y divide-slate-800"></tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- MODAL DE CADASTRO / EDIÇÃO -->
    <div id="modalRegistro" class="fixed inset-0 bg-black/75 hidden items-center justify-center p-4 z-50">
        <div class="card p-6 max-w-lg w-full">
            <h3 class="text-lg font-bold text-white mb-4" id="modalTitulo">Lançar Registro CMPC</h3>
            <form id="formRegistro" onsubmit="salvarRegistro(event)" class="space-y-4 text-sm">
                <input type="hidden" id="regId">
                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="block text-xs text-slate-400 mb-1">Data</label>
                        <input type="date" id="regData" required class="input-field text-white">
                    </div>
                    <div>
                        <label class="block text-xs text-slate-400 mb-1">Programa CMPC</label>
                        <select id="regPrograma" class="input-field text-white">
                            <option value="CUIDAR">CUIDAR (Meta: 4/sem)</option>
                            <option value="IPS">IPS (Meta: 2/sem)</option>
                            <option value="Relatório de Inspeção">Relatório de Inspeção (Meta: 2/sem)</option>
                            <option value="DDS">DDS (Meta: 1/sem)</option>
                            <option value="Auditoria PT/AST">Auditoria PT/AST (Meta: 2/sem)</option>
                            <option value="Reunião Semanal">Reunião Semanal (Meta: 1/sem)</option>
                            <option value="Estatística HHT">Estatística HHT (Meta: 1/sem)</option>
                        </select>
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="block text-xs text-slate-400 mb-1">TST Responsável</label>
                        <input type="text" id="regTST" value="Raquel Carvalho" required class="input-field text-white">
                    </div>
                    <div>
                        <label class="block text-xs text-slate-400 mb-1">Líder Responsável</label>
                        <input type="text" id="regLider" value="Josinei Buchor" required class="input-field text-white">
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="block text-xs text-slate-400 mb-1">Ocorreram Desvios?</label>
                        <select id="regDesvio" class="input-field text-white">
                            <option value="Sim">Sim</option>
                            <option value="Não">Não</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs text-slate-400 mb-1">Qtd Pessoas em Desvio</label>
                        <input type="number" id="regPessoas" value="0" min="0" class="input-field text-white">
                    </div>
                </div>

                <div>
                    <label class="block text-xs text-slate-400 mb-1">Descrição do Desvio / Apontamento</label>
                    <textarea id="regDescricao" rows="3" required class="input-field text-white" placeholder="Descreva a condição observada..."></textarea>
                </div>

                <div class="flex justify-end gap-3 pt-2">
                    <button type="button" onclick="fecharModal()" class="px-4 py-2 bg-slate-700 text-white rounded-lg hover:bg-slate-600">Cancelar</button>
                    <button type="submit" class="px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-500 font-semibold">Salvar Registro</button>
                </div>
            </form>
        </div>
    </div>

    <script>
        let registros = {json_registros};
        const metasCMPC = {json_metas};
        let chartInstance = null;

        function renderizar() {{
            atualizarTabela();
            atualizarMetasCards();
            atualizarGrafico();
            atualizarScore();
        }}

        function atualizarTabela() {{
            const tbody = document.getElementById("tblRegistros");
            tbody.innerHTML = "";
            
            registros.forEach((r, idx) => {{
                tbody.innerHTML += `
                    <tr class="hover:bg-slate-800/50">
                        <td class="p-3 font-mono text-xs text-slate-400">${{r.data}}</td>
                        <td class="p-3 font-semibold text-emerald-400">${{r.programa}}</td>
                        <td class="p-3 text-xs">${{r.responsavel}}<br><span class="text-slate-500">Líder: ${{r.lider}}</span></td>
                        <td class="p-3"><span class="${{r.houve_desvio === 'Sim' ? 'text-amber-400 font-bold' : 'text-slate-400'}}">${{r.houve_desvio}}</span></td>
                        <td class="p-3 text-center">${{r.qtd_pessoas}}</td>
                        <td class="p-3 text-xs text-slate-300 max-w-xs truncate">${{r.descricao}}</td>
                        <td class="p-3 text-center space-x-2">
                            <button onclick="editarRegistro(${{idx}})" class="text-blue-400 hover:text-blue-300 font-bold text-xs">Editar</button>
                            <button onclick="excluirRegistro(${{idx}})" class="text-red-400 hover:text-red-300 font-bold text-xs">Excluir</button>
                        </td>
                    </tr>`;
            }});
        }}

        function atualizarMetasCards() {{
            const container = document.getElementById("cardsMetas");
            container.innerHTML = "";

            Object.keys(metasCMPC).forEach(prog => {{
                const metaObj = metasCMPC[prog];
                const real = registros.filter(r => r.programa === prog).length;
                const pct = Math.min(100, Math.round((real / metaObj.meta_semanal) * 100));

                container.innerHTML += `
                    <div class="card p-3 text-center">
                        <span class="text-[10px] text-slate-400 uppercase font-bold tracking-tight">${{prog}}</span>
                        <div class="text-xl font-extrabold text-white mt-1">${{real}} / ${{metaObj.meta_semanal}}</div>
                        <div class="text-[10px] text-emerald-400 font-semibold">${{pct}}% Atingido</div>
                    </div>`;
            }});
        }}

        function atualizarScore() {{
            let scoreTotal = 0;
            Object.keys(metasCMPC).forEach(prog => {{
                const metaObj = metasCMPC[prog];
                const real = registros.filter(r => r.programa === prog).length;
                const pct = Math.min(100, (real / metaObj.meta_semanal) * 100);
                scoreTotal += (pct * metaObj.peso) / 100;
            }});
            document.getElementById("scoreDisplay").innerText = scoreTotal.toFixed(1) + "%";
        }}

        function atualizarGrafico() {{
            const labels = Object.keys(metasCMPC);
            const realizados = labels.map(p => registros.filter(r => r.programa === p).length);
            const metas = labels.map(p => metasCMPC[p].meta_semanal);

            if (chartInstance) chartInstance.destroy();

            chartInstance = new Chart(document.getElementById('chartMeta'), {{
                type: 'bar',
                data: {{
                    labels: labels,
                    datasets: [
                        {{ label: 'Realizado JB DIAS', data: realizados, backgroundColor: '#10b981', borderRadius: 4 }},
                        {{ label: 'Meta Semanal CMPC', data: metas, backgroundColor: '#374151', borderRadius: 4 }}
                    ]
                }},
                options: {{
                    responsive: true,
                    plugins: {{ legend: {{ labels: {{ color: '#94a3b8' }} }} }},
                    scales: {{
                        x: {{ ticks: {{ color: '#94a3b8' }}, grid: {{ display: false }} }},
                        y: {{ ticks: {{ color: '#94a3b8' }}, grid: {{ color: '#1e293b' }}, beginAtZero: true }}
                    }}
                }}
            }});
        }}

        // ACOES CRUD
        function abrirModal() {{
            document.getElementById("regId").value = "";
            document.getElementById("regData").value = new Date().toISOString().split('T')[0];
            document.getElementById("regDescricao").value = "";
            document.getElementById("modalTitulo").innerText = "Lançar Registro CMPC";
            document.getElementById("modalRegistro").classList.remove("hidden");
            document.getElementById("modalRegistro").classList.add("flex");
        }}

        function fecharModal() {{
            document.getElementById("modalRegistro").classList.add("hidden");
            document.getElementById("modalRegistro").classList.remove("flex");
        }}

        function salvarRegistro(e) {{
            e.preventDefault();
            const id = document.getElementById("regId").value;
            const novo = {{
                id: id !== "" ? registros[id].id : "REG-" + (registros.length + 1),
                data: document.getElementById("regData").value,
                programa: document.getElementById("regPrograma").value,
                empresa: "JB DIAS",
                responsavel: document.getElementById("regTST").value,
                lider: document.getElementById("regLider").value,
                houve_desvio: document.getElementById("regDesvio").value,
                qtd_pessoas: parseInt(document.getElementById("regPessoas").value),
                descricao: document.getElementById("regDescricao").value,
                status: "Concluído"
            }};

            if (id !== "") {{
                registros[id] = novo;
            }} else {{
                registros.unshift(novo);
            }}

            fecharModal();
            renderizar();
        }}

        function editarRegistro(idx) {{
            const r = registros[idx];
            document.getElementById("regId").value = idx;
            document.getElementById("regData").value = r.data;
            document.getElementById("regPrograma").value = r.programa;
            document.getElementById("regTST").value = r.responsavel;
            document.getElementById("regLider").value = r.lider;
            document.getElementById("regDesvio").value = r.houve_desvio;
            document.getElementById("regPessoas").value = r.qtd_pessoas;
            document.getElementById("regDescricao").value = r.descricao;

            document.getElementById("modalTitulo").innerText = "Editar Registro CMPC";
            document.getElementById("modalRegistro").classList.remove("hidden");
            document.getElementById("modalRegistro").classList.add("flex");
        }}

        function excluirRegistro(idx) {{
            if (confirm("Tem certeza que deseja remover este registro?")) {{
                registros.splice(idx, 1);
                renderizar();
            }}
        }}

        // Inicialização
        renderizar();
    </script>
</body>
</html>
"""

    with open(CAMINHO_SAIDA, "w", encoding="utf-8") as f:
        f.write(html_content)

    webbrowser.open(CAMINHO_SAIDA)
    print(f"✅ App JB DIAS EHS gerado com sucesso em: {CAMINHO_SAIDA}")

if __name__ == "__main__":
    compilar_app()