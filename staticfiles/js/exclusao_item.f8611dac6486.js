window.setTimeout(function(){
    // Script para remover mensagens de feedback após 2 segundos
    
    $('.alert').fadeTo(500, 0).slideUp(500, function(){
        $(this).remove();
    });
}, 2000);


$('#deleteModal').on('show.bs.modal', function (event) {
    // Script para mostrar o modal e configurar o botão de apagar com a URL correta
    // Obtém o botão que acionou o modal e a URL

    var button = $(event.relatedTarget) 
    var url = button.data('url') 
    var confirmBtn = $('#confirmDeleteBtn')

    // Atualiza o href do botão de confirmação com a URL do item a ser deletado

    confirmBtn.attr('href', url)
});
