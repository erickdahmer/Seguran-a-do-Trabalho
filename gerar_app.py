import os
import json
import webbrowser
from dashboard import carregar_dados_iniciais
from analisador import calcular_score_governança

CAMINHO_SAIDA = os.path.join(os.path.dirname(__file__), "index.html")

def compilar_app():
    dados_iniciais = carregar_dados_iniciais()
    
    registros = dados_iniciais[0]
    metas = dados_iniciais[1]
    colaboradores = dados_iniciais[2] if len(dados_iniciais) > 2 else []

    score, detalhes = calcular_score_governança(registros, metas)

    json_registros = json.dumps(registros, ensure_ascii=False)
    json_metas = json.dumps(metas, ensure_ascii=False)
    json_colaboradores = json.dumps(colaboradores, ensure_ascii=False)

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
        .input-field {{ background-color: #1f2937; border: 1px solid #374151; color: #ffffff; border-radius: 0.5rem; padding: 0.6rem; width: 100%; font-size: 0.875rem; }}
        .input-field:focus {{ outline: none; border-color: #10b981; }}
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
            
            <div class="flex items-center gap-3">
                <div class="card px-4 py-2 text-center border-emerald-500/40">
                    <span class="text-[10px] text-slate-400 uppercase font-semibold">Índice Compliance CMPC</span>
                    <div id="scoreDisplay" class="text-xl font-black text-emerald-400">{score}%</div>
                </div>
                <button onclick="abrirModalColaborador()" class="bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 px-3 py-2.5 rounded-lg font-semibold text-xs transition flex items-center gap-2">
                    👤 Gerenciar Colaboradores
                </button>
                <button onclick="abrirModal()" class="bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-2.5 rounded-lg font-semibold text-xs transition flex items-center gap-2 shadow-lg shadow-emerald-900/20">
                    ➕ Novo Registro CMPC
                </button>
            </div>
        </div>

        <!-- CARDS DE METAS OBRIGATÓRIAS CMPC -->
        <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3 mb-6" id="cardsMetas"></div>

        <!-- DASHBOARD PRINCIPAL -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
            <div class="card p-5 lg:col-span-2">
                <h2 class="text-base font-semibold text-white mb-4 flex items-center justify-between">
                    <span>📊 Desempenho por Programa de Segurança (Meta Semanal)</span>
                    <span class="text-xs text-slate-400">Metas CMPC</span>
                </h2>
                <canvas id="chartMeta" height="110"></canvas>
            </div>

            <div class="card p-5">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-base font-semibold text-white">👥 Equipe Cadastrada</h2>
                    <button onclick="abrirModalColaborador()" class="text-emerald-400 hover:text-emerald-300 font-bold text-xs">+ Adicionar</button>
                </div>
                <div class="space-y-2 max-h-[220px] overflow-y-auto pr-1" id="listaColaboradoresResumo">
                    <!-- Preenchido via JS -->
                </div>
            </div>
        </div>

        <!-- TABELA INTERATIVA DOS REGISTROS -->
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
                            <th class="p-3">Colaborador / Função</th>
                            <th class="p-3">TST / Líder</th>
                            <th class="p-3">Desvio?</th>
                            <th class="p-3">Pessoas</th>
                            <th class="p-3">Observações / Apontamentos</th>
                            <th class="p-3 text-center">Ações</th>
                        </tr>
                    </thead>
                    <tbody id="tblRegistros" class="divide-y divide-slate-800"></tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- MODAL DE ADICIONAR / REMOVER COLABORADOR -->
    <div id="modalColaborador" class="fixed inset-0 bg-black/80 backdrop-blur-sm hidden items-center justify-center p-4 z-50">
        <div class="card p-6 max-w-md w-full border border-slate-700 shadow-2xl">
            <div class="flex justify-between items-center border-b border-slate-800 pb-3 mb-4">
                <h3 class="text-base font-bold text-white">👤 Gerenciar Colaboradores</h3>
                <button onclick="fecharModalColaborador()" class="text-slate-400 hover:text-white font-bold text-lg">&times;</button>
            </div>

            <form onsubmit="salvarColaborador(event)" class="space-y-4 text-sm mb-6">
                <div>
                    <label class="block text-xs font-semibold text-slate-300 mb-1">Nome Completo</label>
                    <input type="text" id="novoNomeColab" required placeholder="Ex: Roberto Alves" class="input-field">
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-300 mb-1">Cargo / Função</label>
                    <input type="text" id="novoCargoColab" required placeholder="Ex: TST, Operador, Líder Operacional, Mecânico..." class="input-field">
                </div>

                <div class="flex justify-end gap-3 pt-2">
                    <button type="submit" class="w-full py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-500 font-semibold text-xs shadow-md shadow-emerald-900/30">Cadastrar Colaborador</button>
                </div>
            </form>

            <div class="border-t border-slate-800 pt-3">
                <span class="text-xs font-bold text-slate-400 uppercase tracking-wider block mb-2">Lista de Integrantes</span>
                <div class="space-y-2 max-h-48 overflow-y-auto pr-1" id="modalListaColaboradores">
                    <!-- Lista com botão de exclusão -->
                </div>
            </div>
        </div>
    </div>

    <!-- MODAL DE NOVO REGISTRO / EDIÇÃO -->
    <div id="modalRegistro" class="fixed inset-0 bg-black/80 backdrop-blur-sm hidden items-center justify-center p-4 z-50">
        <div class="card p-6 max-w-2xl w-full border border-slate-700 shadow-2xl">
            <div class="flex justify-between items-center border-b border-slate-800 pb-3 mb-4">
                <div>
                    <h3 class="text-lg font-bold text-white" id="modalTitulo">➕ Novo Registro CMPC</h3>
                    <p class="text-xs text-slate-400">Preencha os campos abaixo com dados rápidos dos colaboradores</p>
                </div>
                <button onclick="fecharModal()" class="text-slate-400 hover:text-white font-bold text-lg">&times;</button>
            </div>

            <form id="formRegistro" onsubmit="salvarRegistro(event)" class="space-y-4 text-sm">
                <input type="hidden" id="regId">

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-semibold text-slate-300 mb-1">📅 Data do Registro</label>
                        <input type="date" id="regData" required class="input-field">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-300 mb-1">📌 Programa CMPC</label>
                        <select id="regPrograma" class="input-field">
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

                <div class="p-3 bg-slate-900/60 rounded-lg border border-slate-800 space-y-3">
                    <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider block">👥 Envolvidos & Responsáveis</span>
                    
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        <div>
                            <label class="block text-xs text-slate-400 mb-1">Colaborador Observado</label>
                            <select id="regColaborador" class="input-field text-white"></select>
                        </div>
                        <div>
                            <label class="block text-xs text-slate-400 mb-1">TST Responsável</label>
                            <select id="regTST" class="input-field text-white"></select>
                        </div>
                        <div>
                            <label class="block text-xs text-slate-400 mb-1">Líder Operacional</label>
                            <select id="regLider" class="input-field text-white"></select>
                        </div>
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-semibold text-slate-300 mb-1">⚠ Houve Desvio?</label>
                        <select id="regDesvio" class="input-field">
                            <option value="Sim">Sim</option>
                            <option value="Não">Não</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-300 mb-1">🔢 Qtd. Pessoas Envolvidas</label>
                        <input type="number" id="regPessoas" value="1" min="0" class="input-field">
                    </div>
                </div>

                <div>
                    <label class="block text-xs font-semibold text-slate-300 mb-1">📝 Observação / Descrição do Apontamento</label>
                    <textarea id="regDescricao" rows="3" required class="input-field" placeholder="Descreva apenas os fatos observados, ações corretivas ou notas de campo..."></textarea>
                </div>

                <div class="flex justify-end gap-3 pt-3 border-t border-slate-800">
                    <button type="button" onclick="fecharModal()" class="px-4 py-2 bg-slate-700 text-slate-200 rounded-lg hover:bg-slate-600 font-medium text-xs">Cancelar</button>
                    <button type="submit" class="px-5 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-500 font-semibold text-xs shadow-md shadow-emerald-900/30">Salvar Registro</button>
                </div>
            </form>
        </div>
    </div>

    <script>
        let registros = {json_registros};
        const metasCMPC = {json_metas};
        let colaboradores = {json_colaboradores};
        let chartInstance = null;

        function renderizarColaboradoresResumo() {{
            const div = document.getElementById("listaColaboradoresResumo");
            div.innerHTML = "";
            colaboradores.forEach((c, idx) => {{
                div.innerHTML += `
                    <div class="p-2 bg-slate-800/60 rounded border border-slate-700/50 flex justify-between items-center text-xs">
                        <div>
                            <span class="font-bold text-white block">${{c.nome}}</span>
                            <span class="text-slate-400 text-[11px]">${{c.funcao}}</span>
                        </div>
                        <button onclick="excluirColaborador(${{idx}})" class="text-red-400 hover:text-red-300 font-bold text-xs p-1">🗑️</button>
                    </div>
                `;
            }});
        }}

        function popularModalListaColaboradores() {{
            const div = document.getElementById("modalListaColaboradores");
            div.innerHTML = "";
            if (colaboradores.length === 0) {{
                div.innerHTML = '<span class="text-xs text-slate-500">Nenhum colaborador cadastrado.</span>';
                return;
            }}
            colaboradores.forEach((c, idx) => {{
                div.innerHTML += `
                    <div class="p-2 bg-slate-900/80 rounded border border-slate-800 flex justify-between items-center text-xs">
                        <div>
                            <span class="font-bold text-white">${{c.nome}}</span>
                            <span class="text-slate-400 text-[11px] ml-1">(${{c.funcao}})</span>
                        </div>
                        <button onclick="excluirColaborador(${{idx}})" class="text-red-400 hover:text-red-300 font-bold text-xs">Excluir</button>
                    </div>
                `;
            }});
        }}

        function popularDropdownsColaboradores() {{
            const selColab = document.getElementById("regColaborador");
            const selTST = document.getElementById("regTST");
            const selLider = document.getElementById("regLider");

            selColab.innerHTML = "";
            selTST.innerHTML = "";
            selLider.innerHTML = "";

            if (colaboradores.length === 0) {{
                selColab.innerHTML = '<option value="N/A">Sem colaboradores</option>';
                selTST.innerHTML = '<option value="Raquel Carvalho (TST)">Raquel Carvalho (TST)</option>';
                selLider.innerHTML = '<option value="Josinei Buchor (Líder Operacional)">Josinei Buchor (Líder Operacional)</option>';
                return;
            }}

            colaboradores.forEach(c => {{
                const optText = `${{c.nome}} (${{c.funcao}})`;
                const opt = `<option value="${{c.nome}}">${{optText}}</option>`;
                
                selColab.innerHTML += opt;
                
                const funcUpper = c.funcao.toUpperCase();
                if (funcUpper.includes("TST") || funcUpper.includes("SUPERVISOR") || funcUpper.includes("EHS")) {{
                    selTST.innerHTML += opt;
                }}
                if (funcUpper.includes("LÍDER") || funcUpper.includes("LIDER") || funcUpper.includes("SUPERVISOR") || funcUpper.includes("GERENTE")) {{
                    selLider.innerHTML += opt;
                }}
            }});

            if (!selTST.innerHTML) selTST.innerHTML = selColab.innerHTML;
            if (!selLider.innerHTML) selLider.innerHTML = selColab.innerHTML;
        }}

        function abrirModalColaborador() {{
            document.getElementById("novoNomeColab").value = "";
            document.getElementById("novoCargoColab").value = "";
            popularModalListaColaboradores();
            document.getElementById("modalColaborador").classList.remove("hidden");
            document.getElementById("modalColaborador").classList.add("flex");
        }}

        function fecharModalColaborador() {{
            document.getElementById("modalColaborador").classList.add("hidden");
            document.getElementById("modalColaborador").classList.remove("flex");
        }}

        function salvarColaborador(e) {{
            e.preventDefault();
            const nome = document.getElementById("novoNomeColab").value.trim();
            const funcao = document.getElementById("novoCargoColab").value.trim();

            if (!nome || !funcao) return;

            const novoColab = {{
                id: "COL-" + (colaboradores.length + 1).toString().padStart(3, '0'),
                nome: nome,
                funcao: funcao,
                empresa: "JB DIAS"
            }};

            colaboradores.push(novoColab);
            document.getElementById("novoNomeColab").value = "";
            document.getElementById("novoCargoColab").value = "";
            
            popularModalListaColaboradores();
            popularDropdownsColaboradores();
            renderizarColaboradoresResumo();
        }}

        function excluirColaborador(idx) {{
            if (confirm("Deseja remover " + colaboradores[idx].nome + " da lista de colaboradores?")) {{
                colaboradores.splice(idx, 1);
                popularModalListaColaboradores();
                popularDropdownsColaboradores();
                renderizarColaboradoresResumo();
            }}
        }}

        function renderizar() {{
            atualizarTabela();
            atualizarMetasCards();
            atualizarGrafico();
            atualizarScore();
            renderizarColaboradoresResumo();
        }}

        function atualizarTabela() {{
            const tbody = document.getElementById("tblRegistros");
            tbody.innerHTML = "";
            
            registros.forEach((r, idx) => {{
                tbody.innerHTML += `
                    <tr class="hover:bg-slate-800/50">
                        <td class="p-3 font-mono text-xs text-slate-400">${{r.data}}</td>
                        <td class="p-3 font-semibold text-emerald-400">${{r.programa}}</td>
                        <td class="p-3 text-xs text-white font-medium">${{r.colaborador_envolvido || "N/A"}}</td>
                        <td class="p-3 text-xs">${{r.responsavel}}<br><span class="text-slate-500">Líder: ${{r.lider}}</span></td>
                        <td class="p-3"><span class="${{r.houve_desvio === 'Sim' ? 'bg-amber-500/10 text-amber-400 border border-amber-500/30 text-[11px] px-2 py-0.5 rounded font-bold' : 'text-slate-400'}}">${{r.houve_desvio}}</span></td>
                        <td class="p-3 text-center text-xs font-bold">${{r.qtd_pessoas}}</td>
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

        function abrirModal() {{
            popularDropdownsColaboradores();
            document.getElementById("regId").value = "";
            document.getElementById("regData").value = new Date().toISOString().split('T')[0];
            document.getElementById("regDescricao").value = "";
            document.getElementById("modalTitulo").innerText = "➕ Novo Registro CMPC";
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
                colaborador_envolvido: document.getElementById("regColaborador").value,
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
            popularDropdownsColaboradores();
            const r = registros[idx];
            document.getElementById("regId").value = idx;
            document.getElementById("regData").value = r.data;
            document.getElementById("regPrograma").value = r.programa;
            if (r.colaborador_envolvido) document.getElementById("regColaborador").value = r.colaborador_envolvido;
            if (r.responsavel) document.getElementById("regTST").value = r.responsavel;
            if (r.lider) document.getElementById("regLider").value = r.lider;
            document.getElementById("regDesvio").value = r.houve_desvio;
            document.getElementById("regPessoas").value = r.qtd_pessoas;
            document.getElementById("regDescricao").value = r.descricao;

            document.getElementById("modalTitulo").innerText = "✏️ Editar Registro CMPC";
            document.getElementById("modalRegistro").classList.remove("hidden");
            document.getElementById("modalRegistro").classList.add("flex");
        }}

        function excluirRegistro(idx) {{
            if (confirm("Tem certeza que deseja remover este registro?")) {{
                registros.splice(idx, 1);
                renderizar();
            }}
        }}

        renderizar();
    </script>
</body>
</html>
"""

    with open(CAMINHO_SAIDA, "w", encoding="utf-8") as f:
        f.write(html_content)

    webbrowser.open(CAMINHO_SAIDA)
    print(f"✅ App JB DIAS EHS atualizado e gerado em: {CAMINHO_SAIDA}")

if __name__ == "__main__":
    compilar_app()