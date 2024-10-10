document.getElementById('upload_excel').onchange = function() {
    // Exibir o modal quando o arquivo for selecionado
    $('#processingModal').modal('show');
    // Enviar o formulário com um pequeno atraso
    setTimeout(() => {
        this.form.submit();
    }, 200); // 200 ms de atraso
};  