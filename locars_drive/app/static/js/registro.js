// Arquivo: static/js/registro.js

document.addEventListener('DOMContentLoaded', function() {
    const dataNascInput = document.getElementById('data_nasc');
    const cnhPergunta = document.getElementById('cnh_pergunta');
    const cnhCampoWrapper = document.getElementById('cnh_campo_wrapper');
    const radioSim = document.getElementById('tem_cnh_sim');
    const radioNao = document.getElementById('tem_cnh_nao');
    const cnhInput = document.getElementById('cnh_input');
    
    // NOVO ELEMENTO: Onde a idade será exibida
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
            
            // Ajuste fino para a idade
            if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
                age--; 
            }
        }
        
        // 1. Exibir a idade calculada e dar feedback
        if (age !== null && age >= 0) {
            idadeDisplay.textContent = `Idade: ${age} anos`;
            // Feedback visual: Vermelho se for menor de 16, Verde/Cinza se for 16 ou mais
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
            if (radioSim.checked) {
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
            radioNao.checked = true;
        }
    }

    // --- Event Listeners ---

    // MUDANÇA CRÍTICA: Usa 'input' para maior responsividade
    dataNascInput.addEventListener('input', checkAgeAndCNH); 
    // Mantém o 'change' como fallback (dispara quando o campo perde o foco)
    dataNascInput.addEventListener('change', checkAgeAndCNH); 

    radioSim.addEventListener('change', checkAgeAndCNH);
    radioNao.addEventListener('change', checkAgeAndCNH);

    checkAgeAndCNH();
});