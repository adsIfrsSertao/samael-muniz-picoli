// Leitura do documento e inicializar select2
$(document).ready(function() {
    $('#id_cliente').select2();
    $('#id_produto').select2();
    $('#id_vendedor').select2();

    
    // Função para garantir que os valores sejam positivos
    function positiveValue(input) {
        if (input.value < 0) {
            input.value = Math.abs(input.value);
        }
    }
    $('#quantidade, #valor_unitario, #id_nota_fiscal').on('input', function() {
        positiveValue(this);
        calcularTotal();
    });
});

// Função para calcular o valor total automaticamente
function calcularTotal() {
    var quantidade = document.getElementById("quantidade").value;
    var valorUnitario = document.getElementById("valor_unitario").value; 
    var valorTotal = quantidade * valorUnitario;

    document.getElementById("valor_total").value = valorTotal.toFixed(2);
}