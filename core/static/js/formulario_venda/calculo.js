function calcularTotal() {
    var quantidade = document.getElementById("quantidade").value;
    var valorUnitario = document.getElementById("valor_unitario").value; 
    var valorTotal = quantidade * valorUnitario;

    document.getElementById("valor_total").value = valorTotal.toFixed(2);
}


