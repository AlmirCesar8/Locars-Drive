// Coleção pública para veículos, acessível por todos para locação
const COLLECTION_NAME = 'vehicles';

document.addEventListener('firebase:ready', () => {
    const form = document.getElementById('vehicle-form');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
});

/**
 * Lida com o envio do formulário, valida e salva os dados no Firestore.
 * @param {Event} event - O evento de submissão do formulário.
 */
async function handleFormSubmit(event) {
    event.preventDefault();
    
    const submitBtn = document.getElementById('submit-btn');
    const messageArea = document.getElementById('message-area');

    // Desabilitar o botão e limpar mensagens
    submitBtn.disabled = true;
    submitBtn.textContent = 'Adicionando...';
    messageArea.style.display = 'none';
    messageArea.className = 'message-area';

    // 1. Coletar Dados do Formulário
    const vehicleData = {
        brand: document.getElementById('brand').value.trim(),
        model: document.getElementById('model').value.trim(),
        year: parseInt(document.getElementById('year').value, 10),
        plate: document.getElementById('plate').value.trim().toUpperCase(),
        daily_rate: parseFloat(document.getElementById('daily_rate').value),
        location: document.getElementById('location').value.trim(),
        type: document.getElementById('type').value,
        imageUrl: document.getElementById('imageUrl').value.trim() || 'https://placehold.co/600x400/000/fff?text=LocarsDrive+Veículo', // Placeholder padrão
        status: 'DISPONIVEL', // Novo veículo sempre começa como DISPONIVEL
        km: 0, // Quilometragem inicial
        color: getRandomColor(), // Cor aleatória para identificação visual
        createdAt: window.firebase.serverTimestamp() // Timestamp para ordenação
    };
    
    // 2. Validação Básica (além da validação HTML)
    if (isNaN(vehicleData.daily_rate) || vehicleData.daily_rate <= 0) {
        showMessage('Por favor, insira uma diária válida.', 'error');
        return;
    }
    
    // 3. Salvar no Firestore
    try {
        const vehiclesRef = window.getPublicCollectionRef(COLLECTION_NAME);
        
        if (!vehiclesRef) {
            showMessage('Erro de inicialização: a referência da coleção não está disponível.', 'error');
            return;
        }

        const docRef = await window.firebase.addDoc(vehiclesRef, vehicleData);
        
        // Sucesso
        showMessage(`Veículo "${vehicleData.brand} ${vehicleData.model}" (Placa: ${vehicleData.plate}) adicionado com sucesso! ID: ${docRef.id}`, 'success');
        
        // Limpar formulário após o sucesso
        form.reset();

    } catch (error) {
        console.error("Erro ao adicionar veículo ao Firestore:", error);
        showMessage(`Erro ao salvar: ${error.message}. Tente novamente.`, 'error');
    } finally {
        // Restaurar o botão
        submitBtn.disabled = false;
        submitBtn.textContent = 'Adicionar Veículo à Frota';
    }
}

/**
 * Exibe uma mensagem de status na área de mensagens.
 * @param {string} message - A mensagem a ser exibida.
 * @param {string} type - O tipo de mensagem ('success' ou 'error').
 */
function showMessage(message, type) {
    const messageArea = document.getElementById('message-area');
    messageArea.textContent = message;
    messageArea.className = `message-area message-${type}`;
    messageArea.style.display = 'block';
}

/**
 * Gera uma cor hexadecimal aleatória.
 */
function getRandomColor() {
    const colors = ['#4f46e5', '#10b981', '#f59e0b', '#ef4444', '#3b82f6']; // Cores vibrantes
    const randomIndex = Math.floor(Math.random() * colors.length);
    return colors[randomIndex];
}