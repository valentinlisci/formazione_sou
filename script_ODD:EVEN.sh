#!/bin/bash
#script ODD/EVEN
echo "Benvenuto!"
read -p "Inserisci un numero! non sono accettate lettere o parole: " numero
if [[ "$numero" =~ ^[0-9]+$ ]]; then
    echo "Hai inserito un numero!"
else
    echo "Per favore, inserisci un numero valido."
    exit 1
fi
if (( numero % 2 == 0 )); then
    echo "Il numero $numero è pari."
else
    echo "Il numero $numero è dispari."
fi
for ((i=1; i<=numero; i++)); do
    echo "$i"
done
# :)
