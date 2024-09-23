// Script para remover mensagens de feedback após 2 segundos
window.setTimeout(function(){
    $('.alert').fadeTo(500, 0).slideUp(500, function(){
        $(this).remove();
    });
}, 2000);

// Script para mostrar o modal e configurar o botão de apagar com a URL correta
$('#deleteModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) 
    var url = button.data('url') 
    var confirmBtn = $('#confirmDeleteBtn')
    confirmBtn.attr('href', url)
});

// Filtro de busca dinâmico
document.getElementById('search').addEventListener('input', function() {
    const searchTerm = this.value.toLowerCase();
    const rows = document.querySelectorAll('#list tr');

    rows.forEach(row => {
        const produto = row.querySelector('td:first-child').textContent.toLowerCase();
        if (produto.startsWith(searchTerm)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
});

function filterProducts() {
    const searchInput = document.getElementById('search').value.toLowerCase();
    const productRows = document.querySelectorAll('tbody tr');

    productRows.forEach(row => {
        const productName = row.querySelector('td a').textContent.toLowerCase();
        if (productName.startsWith(searchInput)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
};