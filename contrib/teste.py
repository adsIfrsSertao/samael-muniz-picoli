lista = [10, 4, -5, 7, 8, -5, 9, 5, -6, -5]

# Pegando os 5 últimos itens e garantindo que o 5 seja positivo
ultimos_cinco = [abs(num) if num == -5 else num for num in lista[-5:]]

print(ultimos_cinco)