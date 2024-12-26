document.addEventListener("DOMContentLoaded", function() {

    // Limita o número de caracteres exibidos nas células de texto da lista.
    // Se o conteúdo da célula exceder o limite definido, ele será truncado
    // e "..." será adicionado ao final do texto.
    
    const maxLength = 60; 

    const nomeCells = document.querySelectorAll('#list .fonte-item');
    nomeCells.forEach(cell => {
        if (cell.textContent.length > maxLength) {
            cell.textContent = cell.textContent.slice(0, maxLength - 3) + '...';
        }
    });
});