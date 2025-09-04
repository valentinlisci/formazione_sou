README – Creazione e Registrazione di un Jenkins Agent via REST API

Questo documento descrive passo per passo come:

Ottenere un crumb CSRF e un API token

Creare un nuovo nodo agent tramite le REST API

Recuperare il secret dell’agent

Avviare un container jenkins/inbound-agent che si collega al master

🔹 1. Ottenere il Crumb e salvare i Cookie

Il crumb serve a proteggere Jenkins da attacchi CSRF. Va richiesto al server e passato nelle chiamate successive.

rm -f cookies.txt

curl -c cookies.txt -s -u valentin:valentin \
  http://192.168.56.10:8080/crumbIssuer/api/json


Esempio di risposta:

{"_class":"hudson.security.csrf.DefaultCrumbIssuer","crumb":"ef43a7e57f1e9c82baa871acd93c769af7da3cb492cba44e6961b513c875f02e","crumbRequestField":"Jenkins-Crumb"}

🔹 2. Generare un nuovo API Token

Con il crumb ottenuto puoi generare un API Token (che sostituisce la password nelle chiamate REST).

curl -b cookies.txt -X POST -u valentin:valentin \
  -H "Jenkins-Crumb: ef43a7e57f1e9c82baa871acd93c769af7da3cb492cba44e6961b513c875f02e" \
  -d "newTokenName=my-new-token" \
  http://192.168.56.10:8080/me/descriptorByName/jenkins.security.ApiTokenProperty/generateNewToken


Risultato:

{"status":"ok","data":{"tokenName":"my-new-token","tokenUuid":"12a14746-de83-41e1-9ade-ceec764c8d02","tokenValue":"11b5beaed982f089f8fcacda8d20928349"}}


👉 Salva il valore di tokenValue, in questo caso:

11b5beaed982f089f8fcacda8d20928349

🔹 3. Creare un nuovo Agent Node

Ora puoi creare un nodo Jenkins (che inizialmente sarà offline).

curl -b cookies.txt -X POST -u valentin:11b5beaed982f089f8fcacda8d20928349 \
  -H "Jenkins-Crumb: 8602b1020e4585eb92c974980f99c9021a1cc4fba953eb903faedbb15fb0c2b7" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode 'name=my_agent_name' \
  --data-urlencode 'type=hudson.slaves.DumbSlave$DescriptorImpl' \
  --data-urlencode 
'json={"name":"my_agent_name","nodeDescription":"","numExecutors":"1","remoteFS":"/home/jenkins/agent","labelString":"","mode":"EXCLUSIVE","":""}' 
\
  --data-urlencode 'Submit=OK' \
  "http://192.168.56.10:8080/computer/doCreateItem"

🔹 4. Recuperare l’Agent Secret

Ogni nodo agent ha un secret univoco, necessario per collegarsi.
Puoi estrarlo dal file .jnlp:

curl -s -u valentin:11b5beaed982f089f8fcacda8d20928349 \
  http://192.168.56.10:8080/computer/my_agent_name/jenkins-agent.jnlp \
  | sed -n 's/.*<argument>\([a-z0-9]\{32,\}\)<\/argument>.*/\1/p'


Esempio di risultato:

c9e256b7f0e6d44874d89c64143ef8cf6fef1c420ec003dfc95d37880e2ec8b7


👉 Questo è il tuo agent_secret.

🔹 5. Avviare il Jenkins Agent (Docker)

Con il nome del nodo (my_agent_name) e il secret appena ottenuto, puoi avviare il container:

docker rm -f my-agent

docker run -d --name my-agent \
  jenkins/inbound-agent \
  -url http://192.168.56.10:8080 \
  -name my_agent_name \
  -secret c9e256b7f0e6d44874d89c64143ef8cf6fef1c420ec003dfc95d37880e2ec8b7

🔹 6. Verificare i Log

Per controllare che l’agent sia connesso correttamente:

docker logs -f my-agent


Output atteso:

INFO: Connected
INFO: Agent successfully connected and online


👉 Ora, nella dashboard Jenkins (http://192.168.56.10:8080/computer/), il nodo my_agent_name risulta online.
