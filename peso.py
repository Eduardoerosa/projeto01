pesomenor = 0
pesomaior = 0
for i in range (1,5):
    peso = float(input("digite o peso "))
    if peso == 0:
        print ("o peso e nulo")
    elif i == 1:
        pesomaior = peso
        pesomenor = peso
    else:
        if peso > pesomaior:
            pesomaior = peso
        if peso < pesomenor:
            pesomenor = peso
print (f"o peso maior foi de {pesomaior}")
print (f" o peso menor foi de {pesomenor}")
