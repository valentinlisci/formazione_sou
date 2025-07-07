#!/bin/bash
# Script ODD/EVEN
echo "Benvenuto!"
read -p "Inserisci un numero intero positivo: " numero
if [[ "$numero" =~ ^[1-9][0-9]*$ ]]; then
    echo "Hai inserito un numero valido!"
else
    echo "Per favore, inserisci un numero intero positivo."
    exit 1
fi

for ((i=1; i<=numero; i++)); do
    if (( i % 2 == 0 )); then
        echo "$i è pari."
    else
        echo "$i è dispari."
    fi
done
# :)
