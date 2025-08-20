## 💈 Barbería Borges · Dashboard en tiempo real (Streamlit)

Dashboard de métricas y agenda conectado a PostgreSQL. Interfaz intuitiva, visual y responsive con estilo material.

## 📂 Estructura

- `dashboard/`: código de la app Streamlit (KPIs, gráficos, heatmap y explorador de tablas)
- `schema.sql`: esquema de la base de datos (referencia)

## ✨ Funcionalidades

- **KPIs del día**: citas, clientes únicos e ingresos estimados
- **Citas por barbero**: barras agrupadas (citas/ingresos)
- **Próximas citas**: tabla filtrable por barbero/servicio
- **Heatmap de ocupación**: horas x días (próximas 2 semanas)
- **Top servicios** e **ingresos por día**
- **Explorador de tablas**: vista, filtro por texto y descarga CSV
- **Auto‑refresh** configurable (por defecto 30s)

## 🛠️ Requisitos

- Python 3.10+
- Acceso a PostgreSQL (credenciales vía variables de entorno)

## ⚙️ Variables de entorno

Configúralas en `dashboard/.env` (local) o en tu proveedor (Railway):

```
PGHOST=...           # p.ej. trolley.proxy.rlwy.net
PGPORT=...           # p.ej. 14990
PGDATABASE=...       # p.ej. railway
PGUSER=...
PGPASSWORD=...
REFRESH_INTERVAL_MS=30000
```

## ▶️ Ejecución local

```bash
cd dashboard
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export PGHOST=... PGPORT=... PGDATABASE=... PGUSER=... PGPASSWORD=...
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
# Navega a http://localhost:8501
```

## 🐳 Docker (local)

```bash
docker build -t barberia-dashboard -f dashboard/Dockerfile dashboard
docker run --rm -p 8501:8501 \
  -e PGHOST=$PGHOST -e PGPORT=$PGPORT -e PGDATABASE=$PGDATABASE \
  -e PGUSER=$PGUSER -e PGPASSWORD=$PGPASSWORD \
  barberia-dashboard
```

## 🚀 Despliegue en Railway

1. Conecta el repo `minarkap/barberia-borges` en Railway.
2. Crea un servicio con Dockerfile `dashboard/Dockerfile`.
3. Define variables: `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, `PGPASSWORD`, `REFRESH_INTERVAL_MS`.
4. Deploy de la rama `feat/realtime-dashboard` o de `main` tras el merge del PR.

Más detalles en `dashboard/README_DEPLOY.md`.

## 📦 Dependencias clave

- Streamlit, Plotly, Pandas, psycopg 3, python-dotenv

## 📝 Notas

- Se ha eliminado el boilerplate de Next.js; el proyecto ahora es sólo el dashboard de Streamlit.
- El esquema de referencia está en `schema.sql`.
