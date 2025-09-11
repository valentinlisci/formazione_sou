# Nginx con HTTP Basic Authentication su Kubernetes

Questo progetto dimostra come proteggere Nginx con **HTTP Basic Authentication** all’interno di un cluster Kubernetes (Minikube).

---

## 📂 Struttura del codice

Il file unico `all.yml` contiene tutte le risorse Kubernetes:

- **Secret**  
  Contiene il file `.htpasswd` (codificato in base64) con username e password generati tramite `htpasswd`.

- **ConfigMap**  
  Ridefinisce la configurazione di Nginx abilitando l’autenticazione:
  ```nginx
  server {
      listen 80;
      location / {
          auth_basic "Restricted Content";
          auth_basic_user_file /etc/nginx/auth/.htpasswd;
      }
  }
  ```

- **Pod**  
  Avvia il container `nginx:alpine`, montando:
  - la ConfigMap nella cartella `/etc/nginx/conf.d`
  - il Secret come file `.htpasswd` in `/etc/nginx/auth`

- **Service (LoadBalancer)**  
  Espone Nginx all’esterno del cluster. Con `minikube tunnel` diventa raggiungibile via `http://localhost`.

---

## 🔑 Creazione del Secret

1. Genera file `.htpasswd`:
   ```bash
   htpasswd -c auth utenti
   ```

2. Converti in base64:
   ```bash
   cat auth | base64
   ```

3. Incolla il risultato nella sezione `auth:` del Secret in `all.yml`.

---

## 🚀 Deploy

```bash
# Cancella risorse esistenti
kubectl delete -f all.yml --ignore-not-found

# Applica le nuove configurazioni
kubectl apply -f all.yml

# Avvia tunnel per il LoadBalancer
minikube tunnel
```

Ora apri il browser su:
```
http://localhost
```
Ti verrà chiesto username e password definiti con `htpasswd`.

---

## ✅ Test rapido

- Senza credenziali:
  ```bash
  curl -i http://localhost
  ```
  Risultato: `401 Unauthorized`

- Con credenziali:
  ```bash
  curl -i -u utenti:TUAPASSWORD http://localhost
  ```
  Risultato: `200 OK` con la pagina di default di Nginx.

---

## 📝 Note

- La ConfigMap è minimale: non serve più definire `root` o `index` perché usiamo la pagina di default di Nginx.  
- Il Service di tipo `LoadBalancer` richiede Minikube e il comando `minikube tunnel`.  
- Le risorse sono tutte gestite tramite il file unico `all.yml`.
