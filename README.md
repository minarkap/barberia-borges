# 🪒 Barbería Borges - Dashboard en Tiempo Real

Un dashboard moderno y responsive para gestionar y visualizar datos en tiempo real de la Barbería Borges.

## ✨ Características

- **Dashboard en Tiempo Real**: Actualización automática cada 30 segundos
- **Métricas Visuales**: Estadísticas de citas, ingresos y barberos activos
- **Gráficos Interactivos**: Visualización de datos con Recharts
- **Diseño Material UI**: Interfaz moderna y responsive
- **Notificaciones**: Sistema de alertas en tiempo real
- **Gestión de Citas**: Vista de citas del día y próximas citas
- **Información de la Barbería**: Datos de contacto y horarios

## 🚀 Tecnologías Utilizadas

- **Next.js 14** - Framework de React
- **TypeScript** - Tipado estático
- **Material UI** - Componentes de UI
- **Recharts** - Gráficos interactivos
- **PostgreSQL** - Base de datos
- **Socket.IO** - Comunicación en tiempo real

## 📊 Métricas Disponibles

### Métricas Principales
- **Citas Hoy**: Total de citas programadas para hoy
- **Citas Pendientes**: Citas que aún no se han completado
- **Ingresos Estimados**: Ingresos proyectados para hoy
- **Barberos Activos**: Número de barberos disponibles

### Gráficos y Análisis
- **Citas por Semana**: Distribución de citas por día
- **Servicios Populares**: Análisis de servicios más solicitados
- **Próximas Citas**: Lista de citas futuras con priorización

## 🛠️ Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd barberia_borges
   ```

2. **Instalar dependencias**
   ```bash
   npm install
   ```

3. **Configurar variables de entorno**
   ```bash
   # Las credenciales de la base de datos ya están configuradas en el código
   # Host: trolley.proxy.rlwy.net
   # Puerto: 14990
   # Base de datos: railway
   ```

4. **Ejecutar en desarrollo**
   ```bash
   npm run dev
   ```

5. **Abrir en el navegador**
   ```
   http://localhost:3000
   ```

## 📱 Funcionalidades

### Dashboard Principal
- **Métricas en Tiempo Real**: Actualización automática de estadísticas
- **Gráficos Interactivos**: Hover para ver detalles
- **Responsive Design**: Funciona en móviles y tablets

### Gestión de Citas
- **Vista del Día**: Todas las citas programadas para hoy
- **Estado de Citas**: Completadas, pendientes, próximas
- **Información Detallada**: Cliente, barbero, servicio, precio

### Notificaciones
- **Alertas en Tiempo Real**: Nuevas citas y recordatorios
- **Priorización**: Alta, media, baja prioridad
- **Historial**: Últimas 10 notificaciones

## 🎨 Diseño

### Tema Oscuro
- **Fondo**: Gradiente oscuro (#0a0a0a)
- **Tarjetas**: Efectos de hover y sombras
- **Colores**: Paleta azul con acentos

### Componentes
- **MetricCard**: Tarjetas de métricas con iconos
- **CitasHoy**: Tabla de citas del día
- **Graficos**: Gráficos de barras y dona
- **Notificaciones**: Lista de alertas

## 🔧 API Endpoints

- `GET /api/estadisticas-hoy` - Estadísticas del día actual
- `GET /api/estadisticas-semana` - Estadísticas de la semana
- `GET /api/citas-hoy` - Citas del día actual
- `GET /api/proximas-citas` - Próximas citas
- `GET /api/barberia-info` - Información de la barbería

## 📊 Base de Datos

### Tablas Principales
- **agenda**: Citas de clientes
- **barberos**: Personal de la barbería
- **servicios**: Servicios ofrecidos
- **barberia_info**: Información de la barbería
- **dias**: Días válidos para citas

### Consultas Optimizadas
- Estadísticas en tiempo real
- Agregaciones por día y servicio
- Cálculo de ingresos estimados

## 🚀 Despliegue

### Vercel (Recomendado)
1. Conectar repositorio a Vercel
2. Configurar variables de entorno
3. Desplegar automáticamente

### Otros Proveedores
- **Netlify**: Compatible con Next.js
- **Railway**: Mismo proveedor que la base de datos
- **AWS/GCP**: Configuración manual

## 🔄 Actualizaciones en Tiempo Real

- **Intervalo**: 30 segundos
- **Métricas**: Actualización automática
- **Notificaciones**: Simulación de eventos
- **Gráficos**: Re-renderizado dinámico

## 📱 Responsive Design

- **Desktop**: Layout completo con todas las métricas
- **Tablet**: Reorganización de columnas
- **Mobile**: Stack vertical de componentes

## 🎯 Próximas Mejoras

- [ ] Autenticación de usuarios
- [ ] Gestión de citas (crear/editar/eliminar)
- [ ] Reportes PDF
- [ ] Integración con WhatsApp
- [ ] Dashboard de barberos individuales
- [ ] Sistema de reservas online

## 📞 Soporte

Para soporte técnico o consultas:
- **Email**: [tu-email@ejemplo.com]
- **WhatsApp**: [tu-numero]

---

**Desarrollado con ❤️ para Barbería Borges**
