// Script para remover mensagens de feedback após 2 segundos
window.setTimeout(function(){
    $('.alert').fadeTo(500, 0).slideUp(500, function(){
        $(this).remove();
    });
}, 2000);

// Script para mostrar o modal e configurar o botão de apagar com a URL correta
$('#deleteModal').on('show.bs.modal', function (event) {
    // Obtém o botão que acionou o modal e a URL
    var button = $(event.relatedTarget) 
    var url = button.data('url') 
    var confirmBtn = $('#confirmDeleteBtn')
    // Atualiza o href do botão de confirmação com a URL do item a ser deletado
    confirmBtn.attr('href', url)
});


// Filtro de busca dinâmico
document.getElementById('search').addEventListener('input', function() {
    // Obtém o termo de busca e converte para minúsculas
    const searchTerm = this.value.toLowerCase();
    const rows = document.querySelectorAll('#list tr');

    // Itera sobre as linhas da tabela e exibe ou oculta com base no termo de busca
    rows.forEach(row => {
        const produto = row.querySelector('td:first-child').textContent.toLowerCase();
        if (produto.startsWith(searchTerm)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
});

// Função para filtrar produtos com base na entrada do usuário
function filterProducts() {
    // Obtém o valor do campo de busca e converte para minúsculas
    const searchInput = document.getElementById('search').value.toLowerCase();
    const productRows = document.querySelectorAll('tbody tr');

    // Itera sobre as linhas dos produtos e exibe ou oculta com base no nome do produto
    productRows.forEach(row => {
        const productName = row.querySelector('td a').textContent.toLowerCase();
        if (productName.startsWith(searchInput)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
};