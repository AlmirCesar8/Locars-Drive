// Arquivo: static/js/registro.js

document.addEventListener('DOMContentLoaded', function() {
    const dataNascInput = document.getElementById('data_nasc');
    const cnhPergunta = document.getElementById('cnh_pergunta');
    const cnhCampoWrapper = document.getElementById('cnh_campo_wrapper');
    
    // Agora, estes IDs SÃO ENCONTRADOS graças à correção no HTML
    const radioSim = document.getElementById('tem_cnh_sim');
    const radioNao = document.getElementById('tem_cnh_nao');
    const cnhInput = document.getElementById('cnh_input');
    
    const idadeDisplay = document.getElementById('idade_display'); 

    // Função de animação (mantida)
    function toggleAnimation(element, show) {
        if (show) {
            element.style.opacity = '0';
            element.style.maxHeight = '0';
            element.style.display = 'block';
            element.offsetHeight; 
            element.style.transition = 'opacity 0.5s ease-in-out, max-height 0.5s ease-in-out';
            element.style.opacity = '1';
            element.style.maxHeight = '150px'; 
        } else {
            element.style.transition = 'opacity 0.3s ease-in-out, max-height 0.3s ease-in-out';
            element.style.opacity = '0';
            element.style.maxHeight = '0';
            setTimeout(() => element.style.display = 'none', 300);
            
            if (element === cnhCampoWrapper) {
                cnhInput.required = false;
                cnhInput.value = '';
            }
        }
    }

    function checkAgeAndCNH() {
        const dateValue = dataNascInput.value;
        let age = null; 

        if (dateValue) {
            const birthDate = new Date(dateValue);
            const today = new Date();
            
            age = today.getFullYear() - birthDate.getFullYear();
            const monthDiff = today.getMonth() - birthDate.getMonth();
            
            if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
                age--; 
            }
        }
        
        // 1. Exibir a idade calculada
        if (age !== null && age >= 0) {
            idadeDisplay.textContent = `Idade: ${age} anos`;
            idadeDisplay.style.color = (age < 16) ? '#dc3545' : '#28a745'; 
        } else {
            idadeDisplay.textContent = 'Insira uma data de nascimento válida.';
            idadeDisplay.style.color = 'inherit';
        }

        // 2. Lógica para mostrar/esconder o campo CNH
        if (age !== null && age >= 18) {
            // Mostrar a pergunta CNH
            toggleAnimation(cnhPergunta, true);
            
            // Mostrar o campo de entrada CNH se 'Sim' estiver marcado
            // Este é o bloco que deve estar funcionando:
            if (radioSim && radioSim.checked) {
                toggleAnimation(cnhCampoWrapper, true);
                cnhInput.required = true;
            } else {
                toggleAnimation(cnhCampoWrapper, false);
                cnhInput.required = false;
            }
        } else {
            // Se for menor de 18, esconde tudo e reseta
            toggleAnimation(cnhPergunta, false);
            toggleAnimation(cnhCampoWrapper, false);
            cnhInput.required = false;
            cnhInput.value = '';
            if (radioNao) radioNao.checked = true;
            if (radioSim) radioSim.checked = false;
        }
    }

    // --- Event Listeners ---

    dataNascInput.addEventListener('input', checkAgeAndCNH); 
    dataNascInput.addEventListener('change', checkAgeAndCNH); 

    if (radioSim) radioSim.addEventListener('change', checkAgeAndCNH);
    if (radioNao) radioNao.addEventListener('change', checkAgeAndCNH);

    checkAgeAndCNH();
});