document.addEventListener('DOMContentLoaded', () => {
    // Seleciona todos os grupos de formulário (label + input)
    const formGroups = document.querySelectorAll('.form-group');
    const formContainer = document.querySelector('.form-container');

    // Observa quando o formulário entra na tela para iniciar a animação
    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Se o formulário estiver visível
                formGroups.forEach((group, index) => {
                    // Adiciona a classe que inicia a animação de entrada com atraso
                    setTimeout(() => {
                        group.classList.add('animate-slide-in');
                    }, index * 100); // 100ms de atraso para cada campo
                });
                observer.unobserve(formContainer); // Para de observar após a animação
            }
        });
    }, {
        threshold: 0.1 // Inicia quando 10% do formulário está visível
    });

    // Inicia a observação no container do formulário
    if (formContainer) {
        observer.observe(formContainer);
    }
});