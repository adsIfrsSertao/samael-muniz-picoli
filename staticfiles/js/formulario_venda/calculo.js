console.log('olá');

function calcularTotal() {
    var quantidade = document.getElementById("quantidade").value;
    var valorUnitario = document.getElementById("valor_unitario").value; 
    var valorTotal = quantidade * valorUnitario;

    document.getElementById("valor_total").value = valorTotal.toFixed(2);
}


$(document).ready(function() {
    $('#id_cliente').select2();
    $('#id_produto').select2();
    $('#id_vendedor').select2();

    // Função para transformar valores negativos em positivos
    function positiveValue(input) {
        if (input.value < 0) {
            input.value = Math.abs(input.value);
        }
    }

    // Verificar valores negativos nos campos e inverter para positivo
    $('#quantidade, #valor_unitario, #id_nota_fiscal').on('input', function() {
        positiveValue(this);
    });
});