// Exibe o modal de processamento quando um arquivo Excel é selecionado para upload e envia o formulário 

document.getElementById('upload_excel').onchange = function() {
    // Exibir o modal quando o arquivo for selecionado
    $('#processingModal').modal('show');

    // Envia o formulário
    setTimeout(() => {
        this.form.submit();
    }, 200); // 200 ms de atraso
};  