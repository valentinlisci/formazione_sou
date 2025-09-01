# Ping–Pong Docker Lab — Vagrant

Ambiente Vagrant con **due VM Ubuntu (jammy)** su rete privata che si “passano la palla”:
a turno, **solo una VM** avvia un container `ealen/echo-server` su **porta 8080**, poi lo spegne e
attende che l’altra VM faccia lo stesso. A schermo compaiono le ASCII art **PING**/**PONG**.

## Cos'è
- **VM:** `ping` → 192.168.10.10, `pong` → 192.168.10.20 (rete privata VirtualBox).
- **Provisioning:** installa `docker` e crea `/home/vagrant/esercizio/loop.sh`.
- **Coordinamento:** ogni VM verifica con `curl` `http://IP_altra_VM:8080`; se l’altra è attiva, aspetta.
- **Rotazione:** ciclo infinito; su ogni turno la VM attiva esegue:
  1) avvio `docker run -d -p 8080:80 ealen/echo-server`
  2) attesa ~60s
  3) stop & remove del container
  4) attende che l’altra VM diventi attiva

## Avvio rapido
```bash
vagrant up
vagrant ssh ping   # o: vagrant ssh pong
# lo script viene già creato e referenziato nel provisioning
```

## Verifica
Dal tuo host (se sulla stessa rete host-only), prova:
```
curl http://192.168.10.10:8080
curl http://192.168.10.20:8080
```
Vedrai rispondere **una** VM alla volta (l’altra attende il turno). 

## File principali
- `Vagrantfile` — definizione delle 2 VM e provisioning shell
- `/home/vagrant/esercizio/loop.sh` — logica di rotazione e ASCII art PING/PONG
