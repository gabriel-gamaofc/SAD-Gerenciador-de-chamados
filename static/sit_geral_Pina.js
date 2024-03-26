async function loadChamados() {
    const response = await fetch('/api/sitgeralpina');
    const loadedChamados = await response.json();
    const atendidos = loadedChamados[0]['count(id)']; // Extrai a contagem de atendimentos
    atendimentos_Totais = atendidos;
    console.log("Quantidade de atendimentos:", atendidos);
    return atendidos;
}

async function loadChamados_pri() {
    const response = await fetch('/api/sitprioritarios');
    const load = await response.json();
    const prio = load[0]['count(id)']; // Acesse o primeiro elemento do array
    atendimentos_Totais_pri = prio;
    console.log("Quantidade de prioridade:", prio);
    return prio;
}

async function loadChamados_tma() {
    const response = await fetch('/api/tma');
    const load_tma = await response.json();
    if (load_tma.media_atendimento !== null) {
        const tma = load_tma.media_atendimento;
        tma_global = tma;
        console.log("Tma: ", tma);
        return tma;
    } else {
        console.log("Nenhum TMA encontrado.");
        return null;
    }
}

async function loadMeses() {
    const response = await fetch('/api/grafico_atendimento');
    const data = await response.json();
    totalAtendidosJaneiro = data[0]['total_atendidas_janeiro'];
    totalAtendidosFevereiro = data[0]['total_atendidas_fevereiro'];
    totalAtendidosMarco = data[0]['total_atendidas_marco'];
    console.log("Total atendidos em Janeiro:", totalAtendidosJaneiro);
    console.log("Total atendidos em Fevereiro:", totalAtendidosFevereiro);
    console.log("Total atendidos em Março:", totalAtendidosMarco);
    return { totalAtendidosJaneiro, totalAtendidosFevereiro, totalAtendidosMarco };
}

async function grafpizza() {
    const response = await fetch('/api/graf_pizza');
    const data = await response.json();
    const primeiravia = data[0]['primeiravia'];
    const segundavia = data[0]['segundavia'];
    const outras = data[0]['outros'];
    outras_global = outras;
    primeiravia_global = primeiravia;
    segundavia_global = segundavia;
    console.log("Total atendidos em 1 via:", primeiravia);
    console.log("Total atendidos em 2 via:", segundavia);
    console.log("Total atendidos outros:", outras);
    return { primeiravia_global, segundavia_global, outras_global };
}


async function historico() {
    const response = await fetch('/api/chamados');
    const data = await response.json();
    console.log(data)
    return { data };
}

// Função para preencher a tabela com os dados de manutenção predial
async function preencherTabelaPredial() {
    try {
        const response = await fetch('/api/chamadosPrediais');
        const data = await response.json();
        preencherTabela(data);
        console.log("Predial: ", data);
    } catch (error) {
        console.error('Erro ao carregar os dados de manutenção predial:', error);
    }
}

async function preencherTabelachamados() {
    try {
        const response = await fetch('/api/chamados');
        const data = await response.json();
        preencherTabela(data);
        console.log("Chamados de ti: ", data);
    } catch (error) {
        console.error('Erro ao carregar os dados de manutenção predial:', error);
    }
}


function preencherTabela(data) {
    const tabela = document.getElementById('tabela-chamados').getElementsByTagName('tbody')[0];
    tabela.innerHTML = ''; // Limpa o conteúdo atual da tabela
    data.forEach((item) => {
        const row = tabela.insertRow();
        row.innerHTML = `
            <td>${item.id}</td>
            <td>${item.status}</td>
            <td>${item.Data_Abertura}</td>
            <td>${item.requerente}</td>
            <td>${item.solicitacao}</td>
        `;
    });
}


async function atualizarTabela(data) {
    preencherTabela(data);
}

// Adiciona um event listener para o evento 'change' no seletor do tipo de tabela
document.getElementById('tipoTabela').addEventListener('change', async () => {
    try {
        const tipoTabela = document.getElementById('tipoTabela').value;
        if (tipoTabela === 'chamados') {
            preencherTabelachamados();
        } else if (tipoTabela === 'predial') {
            await preencherTabelaPredial(); // Carrega e preenche a tabela com os dados de manutenção predial
        }
    } catch (error) {
        console.error('Erro ao carregar os dados:', error);
    }
});


/// Carregar e renderizar os dados quando a página carregar
window.addEventListener('load', () => {
    loadChamados()
        .then(totalAtendimentos => {
            document.getElementById('totalAtendimentos').innerText = totalAtendimentos;
            return loadChamados_pri();
        })
        .then(totalPrioritarios => {
            document.getElementById('totalPrioritarios').innerText = totalPrioritarios;
            return loadChamados_tma();
        })
        .then(tma_func => {
            if (tma_func !== null) {
                document.getElementById('tempoMedio').innerText = tma_func;
            }
            return loadMeses();
        })
        .then(() => {
            // Carrega o histórico após carregar os meses
            return historico();
        })
        .then(data => {
            // Preenche a tabela com os dados históricos
            preencherTabela(data.data);
        })
        .then(() => {
            // Dados de exemplo para o gráfico
            const dadosMensais = {
                labels: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
                datasets: [{
                    label: 'Atendimentos por Mês',
                    backgroundColor: 'rgba(54, 162, 235)', // Cor de fundo das barras
                    borderColor: 'rgba(54, 162, 235, 1)', // Cor da borda das barras
                    borderWidth: 1,
                    data: [totalAtendidosJaneiro, totalAtendidosFevereiro, totalAtendidosMarco, 400, 350, 500, 800, 400, 600, 750, 720, 320], // Dados de atendimentos por mês
                }]
            };

            // Configurações do gráfico
            const config = {
                type: 'bar',
                data: dadosMensais,
                options: {
                    scales: {
                        y: {
                            beginAtZero: true                           
                        }
                    }
                },
            };

            // Renderiza o gráfico no canvas
            const ctx = document.getElementById('graficoAtendimentos').getContext('2d');
            new Chart(ctx, config);

            return grafpizza();
        })
        .then(() => {
            // Dados de exemplo para o gráfico de pizza
            const dadosPizza = {
                labels: ['1 via', '2 via', 'Entrega'],
                datasets: [{
                    label: 'Atendimentos por Setor',
                    backgroundColor: ['#ffcd56', '#ff6384', '#36a2eb'], // Cores para cada setor
                    borderColor: 'rgba(255, 255, 255, 0.5)', // Cor da borda dos setores
                    borderWidth: 1,
                    data: [primeiravia_global, segundavia_global, outras_global], // Dados de atendimentos por setor
                }]
            };

            // Configurações do gráfico de pizza
            const configPizza = {
                type: 'pie',
                data: dadosPizza,
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: true,
                            text: 'Tipo de serviço'
                        }
                    }
                },
            };

            // Renderiza o gráfico de pizza no canvas
            const ctxPizza = document.getElementById('graficoPizza').getContext('2d');
            new Chart(ctxPizza, configPizza);

        })
        .catch(error => {
            console.error('Erro ao carregar os dados:', error);
        });
});

