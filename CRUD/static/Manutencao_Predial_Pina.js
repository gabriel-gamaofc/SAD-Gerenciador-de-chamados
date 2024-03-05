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
        <h4 >Orgão: ${chamado.orgao}</h4>
        <h4>Requerente: ${chamado.requerente}</h4>
        <h4>Solicitação: ${chamado.solicitacao}</h4>
        <h4>Status: ${chamado.status}</h4>
        <button class="edit-button action-button" data-chamado-id="${chamado.id}"><i class='bx bx-edit'></i></button>
        <button onclick="deleteChamado(${chamado.id})"><i class='bx bx-trash'></i></button>
      </div>
    `;
    chamadosList.appendChild(chamadoCard);
  });
}
let loadedChamados; // Variável global para armazenar os chamados carregados
async function loadChamados() {
  const response = await fetch('/api/chamadosPrediais');
  const loadedChamados = await response.json();
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
}

function openModal() {
  newFormContainer.style.display = 'block'; // Exibe o formulário
}

function closeModal() {
  newFormContainer.style.display = 'none'; // Oculta o formulário
  // Limpar os campos do formulário
  document.getElementById("orgao").value = "";
  document.getElementById("ip").value = "";
  document.getElementById("tombamento").value = "";
  document.getElementById("status").value = "";
}

// Função para adicionar um novo chamado de T.I.
async function addChamado(event) {
  event.preventDefault();
  const orgao = document.getElementById('orgao').value;
  const requerente = document.getElementById('ip').value;
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
    body: JSON.stringify({ orgao, requerente, solicitacao, status })
  });

  // Recarregar a lista de chamados após adicionar ou atualizar
  loadChamados();
  chamadoForm.reset();
  closeModal();
  location.reload();
}


// Função para excluir um chamado de T.I.
async function deleteChamado(id) {
  await fetch(`/api/chamadosPrediais/${id}`, {
    method: 'DELETE'
  });

  // Recarregar a lista de chamados após excluir
  loadChamados();
}

function editChamado(id, chamados) {
  const chamadoId = parseInt(id); // Convertendo o ID para número inteiro
  const chamado = chamados.find(chamado => chamado.id === chamadoId);
  if (chamado) {
    document.getElementById('orgao').value = chamado.orgao;
    document.getElementById('ip').value = chamado.requerente;
    document.getElementById('tombamento').value = chamado.solicitacao;
    document.getElementById('status').value = chamado.status;
    document.getElementById('chamadoId').value = chamadoId; // Preencher o campo chamadoId com o ID do chamado
    openModal(); // Exibe o formulário preenchido
    //document.getElementById('chamadoId').value = '';
  } else {
    console.error('Chamado não encontrado'); // Adicione uma mensagem de erro caso o chamado não seja encontrado
  }
}



// Carregar os chamados quando a página carregar
window.onload = () => {
  loadChamados();
  chamadoForm.addEventListener('submit', addChamado);

  // Adiciona um evento de clique ao botão "Cancelar" no formulário
  document.getElementById('btnCancel').addEventListener('click', () => {
    console.log("olaaa");
    closeModal(); // Chama a função closeModal() para ocultar o formulário
  });
};
