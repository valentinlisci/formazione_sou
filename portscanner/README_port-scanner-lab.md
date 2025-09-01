# Port Scanner Lab — Vagrant

Ambiente minimale per esercitarsi con **scansioni di porte TCP** in rete locale.
Crea **due VM Ubuntu** collegate su rete privata e installa uno script Bash che usa `nc` (netcat) per verificare se una porta è **aperta** o **chiusa** su un host bersaglio.

## Cosa contiene
- **VM1 (PORTSCANNER1)** — `192.168.10.10`: esegui qui lo scanner.
- **VM2 (PORTSCANNER2)** — `192.168.10.20`: macchina bersaglio (può ospitare servizi da testare, es. HTTP su 80).
- **Script**: `/usr/local/bin/port_scanner.sh` (presente su entrambe), richiede:
  - IP da scansionare
  - Porta iniziale e finale (interi > 0)
  - Scansiona l’intervallo e stampa `APERTA` / `CHIUSA` via `nc -w 1`.

## Requisiti
- **Vagrant** + **VirtualBox**.

## Avvio rapido
```bash
vagrant up                 # crea le 2 VM
vagrant ssh PORTSCANNER1   # entra nella VM1
sudo /usr/local/bin/port_scanner.sh
# Inserisci IP: 192.168.10.20
# Inserisci porta iniziale: 1
# Inserisci porta finale: 1024
```

## Topologia
```
[HOST] ──(Vagrant/VirtualBox)── [VM1 192.168.10.10] ── rete privata ── [VM2 192.168.10.20]
                 esegui scanner  ─────────►   bersaglio porte
```

## Note
- Lo script **valida** gli input (accetta solo interi positivi; chiede di reinserirli se non validi).
- Se su VM2 abiliti un servizio (es. Nginx su **porta 80**), la porta risulterà **APERTA** quando scansionata da VM1.
- Tutta la logica è dichiarata nel `Vagrantfile` tramite **provisioner shell**.
