import os
from datetime import date, datetime, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
import psycopg
from psycopg import sql
from psycopg.rows import dict_row


# ---------- Configuración básica ----------
st.set_page_config(
    page_title="Barbería Borges · Realtime Dashboard",
    page_icon="💈",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_dotenv()


def get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise RuntimeError(f"Falta variable de entorno: {name}")
    return value


def get_connection():
    return psycopg.connect(
        host=get_env("PGHOST"),
        port=get_env("PGPORT"),
        dbname=get_env("PGDATABASE"),
        user=get_env("PGUSER"),
        password=get_env("PGPASSWORD"),
        row_factory=dict_row,
    )


@st.cache_data(ttl=30)
def run_query(sql: str, params: tuple | None = None) -> pd.DataFrame:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall() if cur.description else []
    return pd.DataFrame(rows)


@st.cache_data(ttl=30)
def fetch_barbers() -> pd.DataFrame:
    return run_query(
        """
        SELECT b.id_barbero, b.nombre, b.activo
        FROM public.barberos b
        ORDER BY b.nombre
        """
    )


@st.cache_data(ttl=30)
def fetch_services() -> pd.DataFrame:
    return run_query(
        """
        SELECT s.id_servicio, s.nombre, s.precio, s.duracion_minutos
        FROM public.servicios s
        ORDER BY s.nombre
        """
    )


def kpis_hoy() -> pd.DataFrame:
    return run_query(
        """
        SELECT
            COUNT(*)                             AS citas_hoy,
            COUNT(DISTINCT a.nombre_cliente)     AS clientes_unicos,
            COALESCE(SUM(s.precio), 0)::numeric AS ingresos_estimados
        FROM public.agenda a
        JOIN public.servicios s ON s.id_servicio = a.id_servicio
        WHERE a.fecha = CURRENT_DATE
        """
    )


def kpis_por_barbero_hoy() -> pd.DataFrame:
    return run_query(
        """
        SELECT b.nombre AS barbero,
               COUNT(*) AS citas,
               COALESCE(SUM(s.precio), 0)::numeric AS ingresos
        FROM public.agenda a
        JOIN public.barberos b  ON b.id_barbero = a.id_barbero
        JOIN public.servicios s ON s.id_servicio = a.id_servicio
        WHERE a.fecha = CURRENT_DATE
        GROUP BY b.nombre
        ORDER BY ingresos DESC, citas DESC
        """
    )


def proximas_citas(limit: int = 50) -> pd.DataFrame:
    return run_query(
        """
        SELECT
            (a.fecha::timestamp + a.hora_inicio) AS inicio,
            b.nombre AS barbero,
            a.nombre_cliente,
            a.telefono_cliente,
            s.nombre AS servicio,
            s.precio
        FROM public.agenda a
        JOIN public.barberos b  ON b.id_barbero = a.id_barbero
        JOIN public.servicios s ON s.id_servicio = a.id_servicio
        WHERE (a.fecha::timestamp + a.hora_inicio) >= NOW()
        ORDER BY inicio ASC
        LIMIT %s
        """,
        (limit,),
    )


def ocupacion_heatmap(dias: int = 14) -> pd.DataFrame:
    return run_query(
        """
        SELECT
            a.fecha,
            EXTRACT(HOUR FROM a.hora_inicio)::int AS hora,
            COUNT(*) AS citas
        FROM public.agenda a
        WHERE a.fecha BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '%s days'
        GROUP BY a.fecha, hora
        ORDER BY a.fecha, hora
        """ % dias
    )


def servicios_top(ventana_dias: int = 30) -> pd.DataFrame:
    return run_query(
        """
        SELECT s.nombre AS servicio,
               COUNT(*) AS veces,
               COALESCE(SUM(s.precio), 0)::numeric AS ingresos
        FROM public.agenda a
        JOIN public.servicios s ON s.id_servicio = a.id_servicio
        WHERE a.fecha BETWEEN CURRENT_DATE - INTERVAL '%s days' AND CURRENT_DATE
        GROUP BY s.nombre
        ORDER BY ingresos DESC, veces DESC
        LIMIT 10
        """ % ventana_dias
    )


def ingresos_por_dia(ventana_dias: int = 30) -> pd.DataFrame:
    return run_query(
        """
        SELECT a.fecha::date AS dia,
               COALESCE(SUM(s.precio), 0)::numeric AS ingresos
        FROM public.agenda a
        JOIN public.servicios s ON s.id_servicio = a.id_servicio
        WHERE a.fecha BETWEEN CURRENT_DATE - INTERVAL '%s days' AND CURRENT_DATE + INTERVAL '14 days'
        GROUP BY dia
        ORDER BY dia
        """ % ventana_dias
    )


# ---------- Sidebar ----------
refresh_ms_default = int(os.getenv("REFRESH_INTERVAL_MS", "30000"))
st.sidebar.markdown("## Filtros y ajustes")
refresh_ms = st.sidebar.slider(
    "Auto-Refresh (ms)", min_value=5_000, max_value=120_000, value=refresh_ms_default, step=5_000
)
st.sidebar.caption("La app se recarga automáticamente para datos en tiempo real.")

barberos_df = fetch_barbers()
servicios_df = fetch_services()

barberos_sel = st.sidebar.multiselect(
    "Barberos",
    options=list(barberos_df["nombre"]) if not barberos_df.empty else [],
    default=list(barberos_df["nombre"]) if not barberos_df.empty else [],
)

servicios_sel = st.sidebar.multiselect(
    "Servicios",
    options=list(servicios_df["nombre"]) if not servicios_df.empty else [],
    default=list(servicios_df["nombre"]) if not servicios_df.empty else [],
)

st.sidebar.divider()
ventana_dias = st.sidebar.slider("Ventana para histórico (días)", 7, 90, 30)
st.sidebar.divider()
st.sidebar.markdown(
    "Base de datos: `railway` en `trolley.proxy.rlwy.net`"
)


# ---------- Auto refresh ----------
st_autorefresh_count = st.experimental_rerun  # type: ignore
st_autorefresh = st.experimental_memo  # mute linters
st.experimental_set_query_params(_=datetime.utcnow().timestamp())
st_autorefresh = st.autorefresh if hasattr(st, "autorefresh") else None
if hasattr(st, "autorefresh"):
    st.autorefresh(interval=refresh_ms, key="autorefresh_key")
else:
    # Fallback para versiones sin st.autorefresh
    st.markdown(
        f"<meta http-equiv='refresh' content='{max(int(refresh_ms/1000),1)}' />",
        unsafe_allow_html=True,
    )


# ---------- Header ----------
st.title("💈 Barbería Borges · Realtime Dashboard")
st.caption("KPIs, agenda y actividad en tiempo real")


# ---------- KPIs ----------
kpis = kpis_hoy()
citas_hoy = int(kpis.at[0, "citas_hoy"]) if not kpis.empty else 0
clientes_unicos = int(kpis.at[0, "clientes_unicos"]) if not kpis.empty else 0
ingresos_estimados = float(kpis.at[0, "ingresos_estimados"]) if not kpis.empty else 0.0

col1, col2, col3 = st.columns(3)
col1.metric("Citas hoy", f"{citas_hoy}")
col2.metric("Clientes únicos hoy", f"{clientes_unicos}")
col3.metric("Ingresos estimados hoy", f"€ {ingresos_estimados:,.2f}")


# ---------- Citas por barbero (hoy) ----------
st.subheader("Citas y estimación de ingresos por barbero · hoy")
df_barberos_hoy = kpis_por_barbero_hoy()
if not df_barberos_hoy.empty:
    mask_barberos = df_barberos_hoy["barbero"].isin(barberos_sel) if barberos_sel else True
    fig_bar = px.bar(
        df_barberos_hoy[mask_barberos],
        x="barbero",
        y=["citas", "ingresos"],
        barmode="group",
        labels={"value": "Total", "barbero": "Barbero", "variable": "Métrica"},
        color_discrete_sequence=["#2962FF", "#00C853"],
        height=360,
    )
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.info("No hay citas hoy.")


# ---------- Próximas citas ----------
st.subheader("Próximas citas")
df_next = proximas_citas(50)
if not df_next.empty:
    if barberos_sel:
        df_next = df_next[df_next["barbero"].isin(barberos_sel)]
    if servicios_sel:
        df_next = df_next[df_next["servicio"].isin(servicios_sel)]
    df_next = df_next.rename(columns={"inicio": "Fecha/Hora", "telefono_cliente": "Teléfono"})
    st.dataframe(
        df_next,
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("Sin citas próximas.")


# ---------- Heatmap de ocupación (próximos días) ----------
st.subheader("Ocupación por hora (próximos 14 días)")
df_heat = ocupacion_heatmap(14)
if not df_heat.empty:
    # Pivot para heatmap
    pivot = df_heat.pivot_table(index="hora", columns="fecha", values="citas", fill_value=0)
    fig_heat = px.imshow(
        pivot,
        aspect="auto",
        color_continuous_scale="Blues",
        labels=dict(x="Fecha", y="Hora", color="Citas"),
        height=420,
    )
    st.plotly_chart(fig_heat, use_container_width=True)
else:
    st.info("No hay citas registradas en los próximos días.")


# ---------- Top servicios ----------
st.subheader(f"Top servicios (últimos {ventana_dias} días)")
df_top_serv = servicios_top(ventana_dias)
if not df_top_serv.empty:
    if servicios_sel:
        df_top_serv = df_top_serv[df_top_serv["servicio"].isin(servicios_sel)]
    fig_top = px.bar(
        df_top_serv,
        x="servicio",
        y="ingresos",
        text="veces",
        labels={"ingresos": "Ingresos (€)", "servicio": "Servicio"},
        color_discrete_sequence=["#6200EE"],
        height=360,
    )
    fig_top.update_traces(texttemplate="Veces: %{text}", textposition="outside")
    st.plotly_chart(fig_top, use_container_width=True)
else:
    st.info("Sin datos de servicios en la ventana seleccionada.")


# ---------- Ingresos por día ----------
st.subheader(f"Ingresos por día (± {ventana_dias} días)")
df_ing_dia = ingresos_por_dia(ventana_dias)
if not df_ing_dia.empty:
    fig_line = px.area(
        df_ing_dia,
        x="dia",
        y="ingresos",
        labels={"dia": "Fecha", "ingresos": "Ingresos (€)"},
        color_discrete_sequence=["#2962FF"],
        height=360,
    )
    st.plotly_chart(fig_line, use_container_width=True)
else:
    st.info("No hay información de ingresos en el periodo indicado.")


# ---------- Explorador de tablas ----------
st.subheader("Explorador de tablas")
st.caption("Visualiza el contenido de las tablas principales. Usa el límite para evitar descargas grandes.")

tablas_disponibles = [
    "agenda",
    "barberos",
    "servicios",
    "dias",
    "barberia_info",
    "n8n_chat_histories",
    "n8n_chat_whatsapp",
]

limite_tabla = st.slider("Límite de filas por tabla", 50, 2000, 300, 50)
seleccion = st.multiselect("Selecciona tablas", tablas_disponibles, default=["agenda", "barberos", "servicios"]) 


def fetch_table_generic(table_name: str, limit: int) -> pd.DataFrame:
    # Query segura para identificadores usando psycopg.sql
    with get_connection() as conn:
        with conn.cursor() as cur:
            query = sql.SQL("SELECT * FROM {table} ORDER BY 1 DESC LIMIT %s").format(
                table=sql.Identifier("public", table_name)
            )
            cur.execute(query, (limit,))
            rows = cur.fetchall() if cur.description else []
            return pd.DataFrame(rows)


if seleccion:
    tabs = st.tabs(seleccion)
    for idx, nombre_tabla in enumerate(seleccion):
        with tabs[idx]:
            df_tabla = fetch_table_generic(nombre_tabla, limite_tabla)
            if df_tabla.empty:
                st.info("Sin datos.")
            else:
                # Búsqueda rápida por texto (aplica a columnas tipo string)
                col_texto = [c for c in df_tabla.columns if df_tabla[c].dtype == object]
                filtro = st.text_input("Filtro contiene (aplica a columnas de texto)", key=f"filtro_{nombre_tabla}")
                if filtro and col_texto:
                    mask = pd.Series(False, index=df_tabla.index)
                    for c in col_texto:
                        mask = mask | df_tabla[c].astype(str).str.contains(filtro, case=False, na=False)
                    df_filtrado = df_tabla[mask]
                else:
                    df_filtrado = df_tabla

                st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
                st.download_button(
                    label="Descargar CSV",
                    data=df_filtrado.to_csv(index=False).encode("utf-8"),
                    file_name=f"{nombre_tabla}.csv",
                    mime="text/csv",
                    key=f"dl_{nombre_tabla}",
                )


st.caption("Hecho con Streamlit · Datos en tiempo real desde PostgreSQL")


