// Leitura do documento e inicialização dos elementos Select2, além de definir funções de validação e cálculo

$(document).ready(function() {

    // Inicializa select2 para os campos cliente, produto e vendedor
    $('#id_cliente').select2();
    $('#id_produto').select2();
    $('#id_vendedor').select2();

    
    // Função para garantir que os valores sejam positivos
    function positiveValue(input) {
        if (input.value < 0) {
            input.value = Math.abs(input.value);
        }
    }


    // Aplica a verificação de valor positivo e cálculo do total para os campos quantidade, valor unitário e nota fiscal
    $('#quantidade, #valor_unitario, #id_nota_fiscal').on('input', function() {
        positiveValue(this);
        calcularTotal();
    });
});


// Calcula o valor total automaticamente com base na quantidade e no valor unitário
function calcularTotal() {
    var quantidade = document.getElementById("quantidade").value;
    var valorUnitario = document.getElementById("valor_unitario").value; 
    var valorTotal = quantidade * valorUnitario;

    // Exibe o valor total calculado com 2 casas decimais
    document.getElementById("valor_total").value = valorTotal.toFixed(2);
}