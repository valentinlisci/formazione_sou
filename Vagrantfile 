Vagrant.configure("2") do |config|

  config.vm.define "PORTSCANNER1" do |ping|
    ping.vm.box = "ubuntu/focal64"
    ping.vm.hostname = "vm1"
    ping.vm.network "private_network", ip: "192.168.10.10"

    ping.vm.provision "shell", inline: <<~SHELL
      sudo apt-get update -y
      sudo apt-get install -y netcat-traditional
      sudo apt-get install -y netcat-openbsd
    
      cat > /usr/local/bin/port_scanner.sh << 'EOF'
#!/bin/bash

echo "Verifico quali porte TCP sono in ascolto"
# Qui definisco TARGET_IP in modo che lo script funzioni indipendentemente.
# Nel tuo caso, se esegui lo script su PORTSCANNER1 per scansionare PORTSCANNER2,
# dovrai inserire l'IP di PORTSCANNER2 (192.168.10.20)
read -p "inserisci IP che vuoi scansionare: " TARGET_IP

while true; do
read -p "Inserisci la porta iniziale da scansionare: " START_PORT
    if [[ "$START_PORT" =~ ^[0-9]+$ ]] && (( START_PORT >= 1 )); then
        break
  else
        echo "Errore: Inserisci un numero intero positivo per la porta iniziale. Riprova."
    fi
done

while true; do
read -p "Inserisci la porta finale da scansionare: " END_PORT
if [[ "$END_PORT" =~ ^[0-9]+$ ]] && (( END_PORT >= 1 )); then
        if (( END_PORT < START_PORT )); then
            echo "Errore: La porta finale non può essere minore della porta iniziale. Riprova."
        else
            break
        fi
    else
        echo "Errore: Inserisci un numero intero positivo per la porta finale. Riprova."
    fi
done

echo "--- Avvio Scansione Porte TCP ---"

for ((port=START_PORT; port<=END_PORT; port++)); do
    if echo "" | nc -w 1 "$TARGET_IP" "$port" &> /dev/null; then
        echo "Porta $port: -------APERTA---------"
    else
        echo "Porta $port: CHIUSA"
    fi
done

echo "Scansione completata."

EOF
      chmod +x /usr/local/bin/port_scanner.sh
    SHELL
  end

  config.vm.define "PORTSCANNER2" do |pong|
    pong.vm.box = "ubuntu/focal64"
    pong.vm.hostname = "vm2"
    pong.vm.network "private_network", ip: "192.168.10.20"

    pong.vm.provision "shell", inline: <<~SHELL
      echo "Aggiornamento pacchetti e installazione Nginx su vm2..."
      sudo apt-get update -y
      sudo apt-get install -y netcat-openbsd

      cat > /usr/local/bin/port_scanner.sh << 'EOF'
#!/bin/bash

echo "Verifico quali porte TCP sono in ascolto"
read -p "inserisci IP che vuoi scansionare: " TARGET_IP

while true; do
read -p "Inserisci la porta iniziale da scansionare: " START_PORT
    if [[ "$START_PORT" =~ ^[0-9]+$ ]] && (( START_PORT >= 1 )); then
        break
  else
        echo "Errore: Inserisci un numero intero positivo per la porta iniziale. Riprova."
    fi
done

while true; do
read -p "Inserisci la porta finale da scansionare: " END_PORTs
if [[ "$END_PORT" =~ ^[0-9]+$ ]] && (( END_PORT >= 1 )); then
        if (( END_PORT < START_PORT )); then
            echo "Errore: La porta finale non può essere minore della porta iniziale. Riprova."
        else
            break
        fi
    else
        echo "Errore: Inserisci un numero intero positivo per la porta finale. Riprova."
    fi
done
echo "--- Avvio Scansione Porte TCP ---"

for ((port=START_PORT; port<=END_PORT; port++)); do
    if echo "" | nc -w 1 "$TARGET_IP" "$port" &> /dev/null; then
        echo "Porta $port: -------APERTA---------"
    else
        echo "Porta $port: CHIUSA"
    fi
done

echo "Scansione completata."

EOF
      chmod +x /usr/local/bin/port_scanner.sh
    SHELL
  end

end