# ODD/EVEN — Script Bash

Piccolo script Bash che legge un intero positivo **N** e stampa i numeri da **1** a **N** indicando se ciascuno è **pari** o **dispari**.

## In breve
- **Obiettivo**: esercizio di base su input, ciclo `for` e operatore modulo.
- **Linguaggio**: Bash (compatibile con Linux/macOS).
- **File**: `script_ODD:EVEN.sh`

## Uso rapido
```bash
chmod +x script_ODD:EVEN.sh
./script_ODD:EVEN.sh            # esecuzione interattiva
echo 6 | ./script_ODD:EVEN.sh   # esecuzione non interattiva
```

### Esempio di output
```
Benvenuto!
Inserisci un numero intero positivo: 6
Hai inserito un numero valido!
1 è dispari.
2 è pari.
3 è dispari.
4 è pari.
5 è dispari.
6 è pari.
```

## Comportamento
- Accetta solo interi **> 0**; in caso contrario mostra un messaggio di errore e termina.
- Itera da 1 a N e stampa per ogni numero la sua parità.
