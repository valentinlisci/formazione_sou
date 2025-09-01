# otel-lab

Laboratorio **minimale** per osservabilità: *Flask → OpenTelemetry Collector → Prometheus → Grafana* (+ *Tempo/Jaeger* opzionale).  


---

## Stack & porte

| Componente        | Scopo                         | Porta/Espone        |
|-------------------|-------------------------------|---------------------|
| app-python (Flask)| Endpoint demo + metriche app  | 5000 (`/`, `/metrics`) |
| OTel Collector    | Ingest OTLP + exporter Prom   | 4317 gRPC · 4318 HTTP · 9464 `/metrics` |
| Prometheus        | Scrape Collector              | 9090 (UI)           |
| Grafana           | Dashboarding                  | 3000 (UI)           |
| Tempo/Jaeger (opt)| Backend tracce                | 16686 (Jaeger UI)   |

---

## Architettura (panoramica)

```
[ app-python ] -- OTLP:4317/4318 --> [ OTel Collector ] -- metrics:9464 --> [ Prometheus ] --> [ Grafana ]
                                           \--(opt: OTLP)--> [ Tempo/Jaeger ] --> Grafana Explore
```

---

## Layout repo

```
.
├── Vagrantfile
├── app
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── compose
│   └── podman-compose.yml
├── configs
│   ├── otel-collector-config.yaml
│   ├── prometheus.yml
│   └── tempo.yaml
├── grafana
│   └── provisioning
│       └── datasources
│           └── datasources.yml
└── provisioning
    └── playbook.yml

```

---

## Riferimenti agli STEP della consegna (compatti)

- **STEP 1 — Preparazione**: progetto pensato per **Podman + Podman Compose**. (Cartella: questa repo)
- **STEP 2 — App Python**: `app.py`, `requirements.txt`, `Dockerfile`. Espone **:5000** ed invia **OTLP** a `otel-collector:4317`.
- **STEP 3 — OTel Collector**: `otel-collector-config.yaml` con **receivers** OTLP (4317/4318), **processors** `batch`, `memory_limiter`, **exporter** Prometheus su **:9464** (+ opz. OTLP → Tempo/Jaeger).
- **STEP 4 — Prometheus**: `prometheus.yml` fa scrape di `otel-collector:9464`. UI **:9090**.
- **STEP 5 — Grafana**: `datasources.yml` punta a `http://prometheus:9090`. UI **:3000**. (Opz. datasource Tempo/Jaeger)
- **STEP 6 — Compose**: `podman-compose.yml` definisce i servizi/porte dichiarati sopra. Avvio: `podman-compose up -d`.
- **STEP 7 — Verifica**: `curl http://localhost:5000/` → controlla Collector `/metrics` su **:9464**, Prometheus **:9090**, Grafana **:3000**. (Opz. Jaeger **:16686**)

---
