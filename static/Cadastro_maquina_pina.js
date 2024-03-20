const maquinaForm = document.getElementById('maquinaForm');
const maquinasList = document.getElementById('maquinasList');
const btnOpenForm = document.getElementById('btnOpenForm');
const newFormContainer = document.getElementById('newFormContainer');

function renderMaquinas(maquinas) {
  maquinasList.innerHTML = '';
  maquinas.forEach(maquina => {
    const maquinaCard = document.createElement('div');
    maquinaCard.classList.add('card');
    maquinaCard.innerHTML = `
      <div class="card-child">
        <h3>Orgão: ${maquina.orgao}</h3>
        <h3>IP: ${maquina.ip}</h3>
        <h3>Tombamento: ${maquina.tombamento}</h3>
        <h3>Guichê: ${maquina.guiche}</h3>
        <button class="edit-button action-button" data-maquina-id="${maquina.id}"><i class='bx bx-edit'></i></button>
       <button class="delete-button action-button" onclick="deleteMaquina(${maquina.id})"><i class='bx bx-trash'></i></button>
      </div>
    `;
    maquinasList.appendChild(maquinaCard);
  });
}





async function loadMaquinas() {
  const response = await fetch('/api/maquinas');
  const data = await response.json();
  //console.log('Lista de máquinas:', data);
  renderMaquinas(data);
  //applyCardStyles(); // Chamada da função para aplicar estilos aos cards
   // Agora que maquinas está disponível, podemos chamar editMaquina
   const editButtons = document.querySelectorAll('.edit-button');
   editButtons.forEach(button => {
    button.addEventListener('click', () => {
      const maquinaId = button.dataset.maquinaId;
      //console.log('Maquina ID:', maquinaId); // Adiciona este console.log para verificar o valor de maquinaId
      editMaquina(maquinaId, data); // Passando maquinas como parâmetro
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
  document.getElementById("guiche").value = "";
}



// Função para adicionar uma nova máquina
async function addMaquina(event) {
  event.preventDefault();
  const orgao = document.getElementById('orgao').value;
  const ip = document.getElementById('ip').value;
  const tombamento = document.getElementById('tombamento').value;
  const guiche = document.getElementById('guiche').value;

  // Verifique se há um ID preenchido para determinar se é uma adição ou edição
  const maquinaId = document.getElementById('maquinaId').value;

  let url = '/api/maquinas';
  let method = 'POST';

  // Se houver um ID preenchido, significa que é uma edição
  if (maquinaId) {
    url += `/${maquinaId}`;
    method = 'PUT';
  }

  // Enviar requisição para adicionar ou atualizar a máquina
  await fetch(url, {
    method: method,
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ orgao, ip, tombamento, guiche })
  });

  // Recarregar a lista de máquinas após adicionar ou atualizar
  loadMaquinas();
  maquinaForm.reset();
  closeModal();
}


// Função para excluir uma máquina
async function deleteMaquina(id) {
  await fetch(`/api/maquinas/${id}`, {
    method: 'DELETE'
  });

  // Recarregar a lista de máquinas após excluir
  loadMaquinas();
}

function editMaquina(id, maquinas) {
  console.log("Foi recebido o id ",id);
  const maquinaId = parseInt(id); // Convertendo o ID para número inteiro
  const maquina = maquinas.find(maquina => maquina.id === maquinaId);
  if (maquina) {
    document.getElementById('orgao').value = maquina.orgao;
    document.getElementById('ip').value = maquina.ip;
    document.getElementById('tombamento').value = maquina.tombamento;
    document.getElementById('guiche').value = maquina.guiche;
    document.getElementById('maquinaId').value = maquinaId; // Preencher o campo maquinaId com o ID da máquina
    openModal(); // Exibe o formulário preenchido
    document.getElementById('maquinaId').value = '';
  } else {
    console.error('Máquina não encontrada'); // Adicione uma mensagem de erro caso a máquina não seja encontrada
  }
}



// Carregar as máquinas quando a página carregar
window.onload = () => {
  loadMaquinas();
  maquinaForm.addEventListener('submit', addMaquina);


  // Adiciona um evento de clique ao botão "Cancelar" no formulário
  document.getElementById('btnCancel').addEventListener('click', () => {
    closeModal(); // Chama a função closeModal() para ocultar o formulário
  });
};
