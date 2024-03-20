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
        <h4>ID: ${chamado.id}</h4>
        <h4 >Orgão: ${chamado.orgao}</h4>
        <h4>Requerente: ${chamado.requerente}</h4>
        <h4>Tipo: ${chamado.Tipo}</h4>
        <h4>Status: ${chamado.status}</h4>
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
  const response = await fetch('/api/chamadosPrediais');
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
  const requerente = document.getElementById('ip').value;
  const Tipo = document.getElementById('Tipo').value;
  const solicitacao = document.getElementById('tombamento').value;
  const status = document.getElementById('status').value; 
  const chamadoId = document.getElementById('chamadoId').value; // Verifique se há um ID preenchido para determinar se é uma adição ou edição
  
  //console.log("Teve o id ",chamadoId);
  let url = '/api/chamadosPrediais';
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
    body: JSON.stringify({ orgao, requerente, Tipo, solicitacao, status })
  });

  if (!chamadoId) {
    // Preencher o formulário do Google Sheets após adicionar o chamado ao banco de dados
    await preencherFormularioPython(orgao, requerente,Tipo, solicitacao);
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
  await fetch(`/api/chamadosPrediais/${id}`, {
    method: 'DELETE'
  });

  // Recarregar a lista de chamados após excluir
  loadChamados();
}

async function preencherFormularioPython(orgao, requerente,Tipo,solicitacao) {
  const requestBody = { orgao, requerente,Tipo, solicitacao };

  try {
    const response = await fetch('/api/preencher-formulario-predial', {
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
    document.getElementById('orgao').value = chamado.orgao;
    document.getElementById('ip').value = chamado.requerente;
    document.getElementById('Tipo').value = chamado.Tipo;
    document.getElementById('tombamento').value = chamado.solicitacao;
    document.getElementById('status').value = chamado.status;
    document.getElementById('chamadoId').value = chamadoId; // Preencher o campo chamadoId com o ID do chamado
    openModal(); // Exibe o formulário preenchido
    //document.getElementById('chamadoId').value = '';
  } else {
    console.error('Chamado não encontrado'); // Adicione uma mensagem de erro caso o chamado não seja encontrado
  }
}

function openGerencialForm(chamadoId) {
  const gerencialFormContainer = document.getElementById('gerencialFormContainer');
  const orgao = document.getElementById('orgaoGerencial'); // Corrigido para usar o ID correto
  const requerente = document.getElementById('requerenteGerencial'); // Corrigido para usar o ID correto
  const tipo = document.getElementById('Tipo'); // Corrigido para usar o ID correto
  const solicitacao = document.getElementById('solicitacaoGerencial'); // Corrigido para usar o ID correto
  const status = document.getElementById('statusGerencial'); // Corrigido para usar o ID correto
 

  if (loadedChamados) {
    const chamado = loadedChamados.find(chamado => chamado.id === parseInt(chamadoId));
    if (chamado) {
      
      orgao.value = chamado.orgao;
      requerente.value = chamado.requerente;
      tipo.value = chamado.Tipo;
      solicitacao.value = chamado.solicitacao;
      status.value = chamado.status;
      
      document.getElementById('tipo_acGerencial').value=chamado.Tipo_ac;
      
      document.getElementById('andamentoGerencial').value=chamado.Andamento;
      
      document.getElementById('situacaoGerencial').value=chamado.Situacao;
      
      document.getElementById('obsGerencial').value=chamado.Obs;
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
  
  const orgao = document.getElementById('orgaoGerencial').value;
  const requerente = document.getElementById('requerenteGerencial').value;
  const Tipo = document.getElementById('Tipo').value;
  const solicitacao = document.getElementById('solicitacaoGerencial').value;
  const status = document.getElementById('statusGerencial').value;
  const Tipo_ac = document.getElementById('tipo_acGerencial').value;
  const Andamento = document.getElementById('andamentoGerencial').value;
  const Situacao = document.getElementById('situacaoGerencial').value;
  const OBS = document.getElementById('obsGerencial').value;

  //console.log("ChamadoID: ", chamadoId, "Orgao: ", orgao, "Requerente: ", requerente, "Tipo ", Tipo, "Solicitação: ", solicitacao, " Status: ", status, " Tipo: ", Tipo_ac, " Andamento: ", Andamento, " Situação: ", Situacao, " obs: ", OBS);

  if (!orgao || !requerente || !Tipo || !solicitacao || !status || !Tipo_ac || !Andamento || !Situacao || !OBS) {
    console.error('Algum elemento não foi encontrado no DOM.');

    // Verificar e definir campos vazios como "N/A"
    if (!Tipo_ac) alert("Diga qual o tipo de ação!");
    if (!Andamento) document.getElementById('andamentoGerencial').value = 'N/A';
    if (!Situacao)document.getElementById('situacaoGerencial').value = 'N/A';
    if (!OBS)  document.getElementById('obsGerencial').value = 'N/A';
    alert("Aperte novamente para salvar!")

    return;
}

  let url = `/api/chamadosPrediais/${chamadoId}`;
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
      body: JSON.stringify({ orgao, requerente, Tipo, solicitacao, status, Tipo_ac, Andamento, Situacao, OBS })
    });

    if (response.ok) {
      alert('Chamado atualizado com sucesso!');
      closeModal_gerencial();
      loadChamados();
      location.reload();
    } else {
      console.error('Erro ao atualizar o chamado:', response.statusText);
    }
  } catch (error) {
    console.error('Erro ao atualizar o chamado:', error);
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


function filterChamadosPorTipo() {
  const andamentoInput = document.getElementById('tipoFilter');
  const selectedAndamento = andamentoInput.value;

  

  if (selectedAndamento === 'todos') {
    renderChamados(loadedChamados); // Recarrega todos os chamados
    
    return;
  }

  const filteredChamados = loadedChamados.filter(chamado => chamado.Tipo === selectedAndamento);

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
document.getElementById('tipoFilter').addEventListener('change', filterChamadosPorTipo);


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
