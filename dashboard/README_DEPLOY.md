### Despliegue rápido

#### Local

```bash
cd /Users/JoseSanchis/Projects/barberia_borges/dashboard
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export PGHOST=trolley.proxy.rlwy.net PGPORT=14990 PGDATABASE=railway PGUSER=postgres PGPASSWORD=iORHsTPrDEkVhuaOrvJIcygpoAvfpkid
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

#### Docker (local)

```bash
cd /Users/JoseSanchis/Projects/barberia_borges
docker build -t barberia-dashboard -f dashboard/Dockerfile dashboard
docker run --rm -p 8501:8501 \
  -e PGHOST=trolley.proxy.rlwy.net -e PGPORT=14990 -e PGDATABASE=railway \
  -e PGUSER=postgres -e PGPASSWORD=TU_PASSWORD \
  barberia-dashboard
```

#### Railway

1. Desde la raíz del repo:
```bash
railway init
railway up --service dashboard --buildfrom docker --dockerfile dashboard/Dockerfile
```
2. En el panel de Railway, añade variables de entorno del Postgres: `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, `PGPASSWORD` y opcional `REFRESH_INTERVAL_MS`.
3. Publica. La app expondrá el puerto `8501` (Streamlit) y estará accesible por la URL que te dé Railway.


