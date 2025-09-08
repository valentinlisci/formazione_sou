# Estrazione dei valori con `grep -P` utilizzando esclusivamente lookahead

---

## 1. Crumb da `crumb.json`

**File di input:**
```json
{"crumb":"ab12cd34ef56gh78","crumbRequestField":"Jenkins-Crumb"}
```

**Comando:**
```bash
grep -Po '"crumb":"[a-z0-9]+(?=")' crumb.json
```

**Output atteso:**
```
"crumb":"ab12cd34ef56gh78
```

**Spiegazione regex :**

| Parte regex          | Significato                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| `"crumb":"`           | Inizio del match, include la chiave `crumb`.                               |
| `[a-z0-9]+`           | Uno o più caratteri alfanumerici minuscoli (il valore del crumb).          |
| `(?=")`               | Lookahead positivo: assicura che subito dopo ci sia `"` (fine valore JSON). |

---

## 2. API Token da `token.json`

**File di input:**
```json
{"data":{"tokenName":"my-new-token","tokenValue":"abcd1234efgh5678ijkl9012mnop3456"}}
```

**Comando:**
```bash
grep -Po '"tokenValue":"[a-z0-9]+(?=")' token.json
```

**Output atteso:**
```
"tokenValue":"abcd1234efgh5678ijkl9012mnop3456
```

**Spiegazione regex :**

| Parte regex           | Significato                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| `"tokenValue":"`       | Inizio del match, include la chiave `tokenValue`.                          |
| `[a-z0-9]+`            | Matcha il valore del token (caratteri alfanumerici).                       |
| `(?=")`                | Lookahead positivo: assicura che subito dopo ci sia `"` (fine valore JSON). |

---

## 3. Agent Secret da `jnlp.xml`

**File di input:**
```xml
<jnlp>
  <application-desc>
    <argument>my-agent</argument>
    <argument>c9e256b7f0e6d44874d89c64143ef8cf6</argument>
  </application-desc>
</jnlp>
```

**Comando:**
```bash
grep -Po '<argument>[a-z0-9]{32,}(?=</argument>)' jnlp.xml
```

**Output atteso:**
```
<argument>c9e256b7f0e6d44874d89c64143ef8cf6
```

**Spiegazione regex :**

| Parte regex            | Significato                                                                 |
|-------------------------|-----------------------------------------------------------------------------|
| `<argument>`            | Inizio del match, include il tag XML `<argument>`.                         |
| `[a-z0-9]{32,}`         | Matcha almeno 32 caratteri alfanumerici (tipico secret Jenkins).           |
| `(?=</argument>)`       | Lookahead positivo: assicura che il match sia seguito da `</argument>`.    |

---
