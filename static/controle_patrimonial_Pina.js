const chamadoForm = document.getElementById('chamadoForm');
const chamadosList = document.getElementById('chamadosList');
const btnOpenForm = document.getElementById('btnOpenForm');
const newFormContainer = document.getElementById('newFormContainer');

function renderChamados(chamados) {
  const chamadosList = document.getElementById('chamadosList');
  if (!chamadosList) {
    console.error("Elemento 'chamadosList' não encontrado.");
    return;
  }

  chamadosList.innerHTML = '';
  chamados.forEach(chamado => {
    const chamadoCard = document.createElement('div');
    chamadoCard.classList.add('card');
    
    chamadoCard.innerHTML = `
      <div class="card-child">
        <h6>ID: ${chamado.id}</h6>
        <h6 >Orgão: ${chamado.orgao}</h6>
        <h6>Requerente: ${chamado.requerente}</h6>
        <h6>Monitor 1 Tombamento: ${chamado.monitor1_tombamento}</h6>
        <h6>Gabinete  Tombamento:  ${chamado.gabiente_tombamento}</h6>
        <h6> Status: ${chamado.status}</h6>
        <!--<button class="edit-button action-button" data-chamado-id="${chamado.id}"><i class='bx bx-edit'></i></button>-->
        <!-- <button onclick="deleteChamado(${chamado.id})"><i class='bx bx-trash'></i></button>-->
        <button class="open-gerencial-form-button action-button" data-chamado-id="${chamado.id}"> <i class="fas fa-cogs"></i></button>
      </div>
    `;
    chamadosList.appendChild(chamadoCard);
  });
}
let loadedChamados; // Variável global para armazenar os chamados carregados
async function loadChamados() {
  const response = await fetch('/api/controlepatrimonialpina');
  loadedChamados = await response.json();
  //console.log("Lista ",loadedChamados);
  renderChamados(loadedChamados);
  //applyCardStyles();

  

  const editButtons = document.querySelectorAll('.edit-button');
  editButtons.forEach(button => {
    button.addEventListener('click', () => {
      const chamadoId = button.dataset.chamadoId;
      editChamado(chamadoId, loadedChamados); // Passando loadedChamados como parâmetro
    });
  });

  const Gerencialbtn = document.querySelectorAll('.open-gerencial-form-button');
  Gerencialbtn.forEach(button => {
    button.addEventListener('click', () => {
    const chamadoId = button.dataset.chamadoId;
    openGerencialForm(chamadoId, loadedChamados); // Passando loadedChamados como parâmetro
    });
  });
}

function openModal() {
  newFormContainer.style.display = 'block'; // Exibe o formulário
}

function closeModal() {
  newFormContainer.style.display = 'none'; // Oculta o formulário
  // Limpar os campos do formulário
  document.getElementById("orgao").value = "";
  document.getElementById("ip").value = "";
  document.getElementById("Tipo").value = "";
  document.getElementById("tombamento").value = "";
  document.getElementById("status").value = "";
}

function closeModal_gerencial() {
  const gerencialFormContainer = document.getElementById('gerencialFormContainer');
  const body = document.querySelector('body');

  gerencialFormContainer.style.display = 'none'; // Ocultar o formulário gerencial

  // Remover classe do body quando o formulário gerencial for fechado
  body.classList.remove('modal-open');
}

// Função para adicionar um novo chamado de T.I.
async function addChamado(event) {
  event.preventDefault();
  // Adicionar sobreposição para bloquear as interações do usuário
  const overlay = document.createElement('div');
  overlay.classList.add('overlay');
  document.body.appendChild(overlay);
  
   // Adicionar indicador de carregamento
  const loader = document.createElement('div');
  loader.classList.add('loader');
  document.body.appendChild(loader);
 
 
 
   // aqui cpmeça a funçãop
  try{
  const orgao = document.getElementById('orgao').value;
  const requerente = document.getElementById('requerente').value;
  const monitor1_tomb = document.getElementById('mon1tomb').value;
  const  monitor1_serie = document.getElementById('mon1serie').value;
  const  monitor2_tomb = document.getElementById('mon2tomb').value;
  const monitor2_serie = document.getElementById('mon2serie').value;
  const gabiente_Tom = document.getElementById('gabtomb').value;
  const gabiente_serie = document.getElementById('gabser').value;
  const chamadoId = document.getElementById('chamadoId').value; // Verifique se há um ID preenchido para determinar se é uma adição ou edição
  
  //console.log("Teve o id ",chamadoId);
  let url = '/api/controlepatrimonialpina';
  let method = 'POST';

  // Se houver um ID preenchido, significa que é uma edição
  if (chamadoId) {
    url += `/${chamadoId}`;
    method = 'PUT';
  }

  // Enviar requisição para adicionar ou atualizar o chamado
  await fetch(url, {
    method: method,
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ orgao, requerente,monitor1_tomb, monitor1_serie, monitor2_tomb,monitor2_serie,gabiente_Tom,gabiente_serie })
  });

  
  
  if (!chamadoId) {
    // Preencher o formulário do Google Sheets após adicionar o chamado ao banco de dados
    await preencher_formulario_controle_patrimonial(orgao, requerente,monitor1_tomb, monitor1_serie, monitor2_tomb,monitor2_serie,gabiente_Tom,gabiente_serie);
  }

  // Recarregar a lista de chamados após adicionar ou atualizar
  loadChamados();
  chamadoForm.reset();
  closeModal();
  location.reload();
} catch (error) {
  console.error('Erro ao atualizar o chamado:', error);

  // Em caso de erro, garantir que a sobreposição e o indicador de carregamento sejam removidos
  document.body.removeChild(overlay);
  document.body.removeChild(loader);
}
}

// Função para lidar com a busca do chamado por ID
function searchChamado() {
  const searchInput = document.getElementById('searchChamado');
  const searchValue = searchInput.value.trim();

  if (searchValue === '') {
    alert('Por favor, insira um ID de chamado válido.');
    return;
  }

  const chamadoId = parseInt(searchValue);
  const chamado = loadedChamados.find(chamado => chamado.id === chamadoId);

  if (chamado) {
    renderChamados([chamado]); // Renderiza apenas o chamado encontrado
    const editButtons = document.querySelectorAll('.edit-button');
    editButtons.forEach(button => {
      button.addEventListener('click', () => {
        const chamadoId = button.dataset.chamadoId;
        editChamado(chamadoId, loadedChamados); // Passando loadedChamados como parâmetro
      });
    });
  
    const Gerencialbtn = document.querySelectorAll('.open-gerencial-form-button');
    Gerencialbtn.forEach(button => {
      button.addEventListener('click', () => {
        const chamadoId = button.dataset.chamadoId;
        openGerencialForm(chamadoId, loadedChamados); // Passando loadedChamados como parâmetro
      });
    });
  } else {
    alert('Nenhum chamado encontrado com o ID especificado.');
  }

  searchInput.value = ''; // Limpa o campo de pesquisa após a busca
}

// Adiciona um evento de clique ao botão de pesquisa
document.getElementById('btnSearchChamado').addEventListener('click', searchChamado);



// Função para excluir um chamado de T.I.
async function deleteChamado(id) {
  await fetch(`/api/controlepatrimonialpina/${id}`, {
    method: 'DELETE'
  });

  // Recarregar a lista de chamados após excluir
  loadChamados();
}

async function preencher_formulario_controle_patrimonial(orgao, requerente,monitor1_tomb, monitor1_serie, monitor2_tomb,monitor2_serie,gabiente_Tom,gabiente_serie) {
  const requestBody = { orgao, requerente,monitor1_tomb, monitor1_serie, monitor2_tomb,monitor2_serie,gabiente_Tom,gabiente_serie };
 
  try {
    const response = await fetch('/api/preencher-formulario-controle-patrimonial', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody)
    });

    if (response.ok) {
      console.log('Script Python executado com sucesso.');
      alert("Chamado Aberto Com sucesso")
    } else {
      console.error('Erro ao executar o script Python:', response.statusText);
    }
  } catch (error) {
    console.error('Erro ao fazer a solicitação para executar o script Python:', error);
  }
}

function editChamado(id, chamados) {
  const chamadoId = parseInt(id); // Convertendo o ID para número inteiro
  const chamado = chamados.find(chamado => chamado.id === chamadoId);
  if (chamado) {
    orgao = document.getElementById('orgao').value; // Corrigido para usar o ID correto
    requerente = document.getElementById('Requerente').value; // Corrigido para usar o ID correto
    monitor1_tomb = document.getElementById('mon1tomb').value;
    monitor1_serie = document.getElementById('mon1serie').value;
    monitor2_tomb = document.getElementById('mon2tomb').value;
    monitor2_serie = document.getElementById('mon2serie').value;
    gabiente_Tom = document.getElementById('gabtomb').value;
    gabiente_serie = document.getElementById('gabser').value;
    document.getElementById('chamadoId').value = chamadoId; // Preencher o campo chamadoId com o ID do chamado
    openModal(); // Exibe o formulário preenchido
    //document.getElementById('chamadoId').value = '';
  } else {
    console.error('Chamado não encontrado'); // Adicione uma mensagem de erro caso o chamado não seja encontrado
  }
}

function openGerencialForm(chamadoId) {
  const gerencialFormContainer = document.getElementById('gerencialFormContainer');
  const orgao = document.getElementById('orgao_ger'); // Corrigido para usar o ID correto
  const requerente = document.getElementById('requerente_ger'); // Corrigido para usar o ID correto
  const monitor1_tomb = document.getElementById('mon1tomb_ger');
  const monitor1_serie = document.getElementById('mon1serie_ger')
  const monitor2_tomb = document.getElementById('mon2tomb_ger')
  const monitor2_serie = document.getElementById('mon2serie_ger')
  const gabiente_Tom = document.getElementById('gabtomb_ger')
  const gabiente_serie = document.getElementById('gabser_ger')
  const status = document.getElementById('status')
 

  if (loadedChamados) {
    const chamado = loadedChamados.find(chamado => chamado.id === parseInt(chamadoId));
    if (chamado) {
      orgao.value = chamado.orgao;
      requerente.value = chamado.requerente;
      monitor1_tomb.value = chamado.monitor1_tombamento;
      monitor1_serie.value = chamado.monitor1_serie;
      monitor2_tomb.value = chamado.monitor2_tombamento;
      monitor2_serie.value = chamado.monitor2_serie;
      gabiente_Tom.value = chamado.gabiente_tombamento;
      gabiente_serie.value = chamado.gabiente_serie;
      status.value = chamado.status;
      gerencialFormContainer.style.display = 'block';
      gerencialFormContainer.addEventListener('submit', event => saveGerencialForm(event, chamadoId)); // Adiciona chamadoId como parâmetro
    } else {
      console.error('Chamado não encontrado');
    }
  } else {
    console.error('Lista de chamados não carregada');
  }
}

async function saveGerencialForm(event, chamadoId) {
  event.preventDefault();
  
  const orgao = document.getElementById('orgao_ger').value; // Corrigido para usar o ID correto
  const requerente = document.getElementById('requerente_ger').value; // Corrigido para usar o ID correto
  const monitor1_tomb = document.getElementById('mon1tomb_ger').value;
  const monitor1_serie = document.getElementById('mon1serie_ger').value;
  const monitor2_tomb = document.getElementById('mon2tomb_ger').value;
  const monitor2_serie = document.getElementById('mon2serie_ger').value;
  const gabiente_Tom = document.getElementById('gabtomb_ger').value;
  const gabiente_serie = document.getElementById('gabser_ger').value;
  const status = document.getElementById('status_ger').value;

  //console.log("ChamadoID: ", chamadoId, "Orgao: ", orgao, "Requerente: ", requerente, "Tipo ", Tipo, "Solicitação: ", solicitacao, " Status: ", status, " Tipo: ", Tipo_ac, " Andamento: ", Andamento, " Situação: ", Situacao, " obs: ", OBS);

  if (!orgao || !requerente || !monitor1_tomb || !monitor1_serie || !gabiente_Tom || !gabiente_serie || !status) {
    console.error('Algum elemento não foi encontrado no DOM.');


    return;
}

  let url = `/api/controlepatrimonialpina/${chamadoId}`;
  let method = 'PUT';
  // Adicionar sobreposição para bloquear as interações do usuário
  
  const overlay = document.createElement('div');
  overlay.classList.add('overlay');
  document.body.appendChild(overlay);
 
  // Adicionar indicador de carregamento
  const loader = document.createElement('div');
  loader.classList.add('loader');
  document.body.appendChild(loader);
  try {
    const response = await fetch(url, {
      method: method,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ orgao, requerente,monitor1_tomb, monitor1_serie, monitor2_tomb,monitor2_serie,gabiente_Tom,gabiente_serie,status })
    });

    if (response.ok) {
      alert('Equipamento atualizado com sucesso!');
      closeModal_gerencial();
      loadChamados();
      location.reload();
    } else {
      console.error('Erro ao atualizar o Equipamento:', response.statusText);
    }
  } catch (error) {
    console.error('Erro ao atualizar o Equipamento:', error);
    // Em caso de erro, garantir que a sobreposição e o indicador de carregamento sejam removidos
    document.body.removeChild(overlay);
    document.body.removeChild(loader);
  }
}

function filterChamadosPorAndamento() {
  const andamentoInput = document.getElementById('statusFilter');
  const selectedAndamento = andamentoInput.value;

  

  if (selectedAndamento === 'todos') {
    renderChamados(loadedChamados); // Recarrega todos os chamados
    
    return;
  }

  const filteredChamados = loadedChamados.filter(chamado => chamado.status === selectedAndamento);

  if (filteredChamados.length > 0) {
    renderChamados(filteredChamados);

    const editButtons = document.querySelectorAll('.edit-button');
    editButtons.forEach(button => {
      button.addEventListener('click', () => {
        const chamadoId = button.dataset.chamadoId;
        editChamado(chamadoId, filteredChamados); // Passando os chamados filtrados como parâmetro
      });
    });

    const Gerencialbtn = document.querySelectorAll('.open-gerencial-form-button');
    Gerencialbtn.forEach(button => {
      button.addEventListener('click', () => {
        const chamadoId = button.dataset.chamadoId;
        openGerencialForm(chamadoId, filteredChamados); // Passando os chamados filtrados como parâmetro
      });
    });
  }else{
    alert("Nenhum chamado nessa situação")
  } 
}

// Adiciona um evento de mudança ao combobox de filtro por andamento
document.getElementById('statusFilter').addEventListener('change', filterChamadosPorAndamento);





function filterChamadosPorOrgao() {
  const andamentoInput = document.getElementById('orgaoFilter');
  const selectedAndamento = andamentoInput.value;

  

  if (selectedAndamento === 'todos') {
    renderChamados(loadedChamados); // Recarrega todos os chamados
    
    return;
  }

  const filteredChamados = loadedChamados.filter(chamado => chamado.orgao === selectedAndamento);

  if (filteredChamados.length > 0) {
    renderChamados(filteredChamados);

    const editButtons = document.querySelectorAll('.edit-button');
    editButtons.forEach(button => {
      button.addEventListener('click', () => {
        const chamadoId = button.dataset.chamadoId;
        editChamado(chamadoId, filteredChamados); // Passando os chamados filtrados como parâmetro
      });
    });

    const Gerencialbtn = document.querySelectorAll('.open-gerencial-form-button');
    Gerencialbtn.forEach(button => {
      button.addEventListener('click', () => {
        const chamadoId = button.dataset.chamadoId;
        openGerencialForm(chamadoId, filteredChamados); // Passando os chamados filtrados como parâmetro
      });
    });
  }else{
    alert("Nenhum chamado nessa situação")
  } 
}

// Adiciona um evento de mudança ao combobox de filtro por andamento
document.getElementById('orgaoFilter').addEventListener('change', filterChamadosPorOrgao);



// Carregar os chamados quando a página carregar
window.onload = () => {
  loadChamados();
  chamadoForm.addEventListener('submit', addChamado);

  // Adiciona um evento de clique ao botão "Cancelar" no formulário
  document.getElementById('btnCancel').addEventListener('click', () => {
    console.log("olaaa");
    closeModal(); // Chama a função closeModal() para ocultar o formulário
  });

  // Adiciona um evento de clique ao botão "Cancelar" no formulário
  document.getElementById('btnCancelGerencial').addEventListener('click', () => {
    console.log("olaaa");
    closeModal_gerencial(); // Chama a função closeModal() para ocultar o formulário
  });

};
