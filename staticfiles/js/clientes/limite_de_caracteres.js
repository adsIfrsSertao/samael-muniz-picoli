document.addEventListener("DOMContentLoaded", function() {
    const maxLength = 60; // Número máximo de caracteres

    const nomeCells = document.querySelectorAll('#list .fonte-item');
    nomeCells.forEach(cell => {
        if (cell.textContent.length > maxLength) {
            cell.textContent = cell.textContent.slice(0, maxLength - 3) + '...';
        }
    });
});