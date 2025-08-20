'use client'

import { useState, useEffect } from 'react'
import { 
  Box, 
  Container, 
  Grid, 
  Typography, 
  AppBar, 
  Toolbar,
  IconButton,
  Chip,
  CircularProgress
} from '@mui/material'
import { 
  Refresh as RefreshIcon,
  Schedule as ScheduleIcon,
  TrendingUp as TrendingUpIcon,
  People as PeopleIcon,
  AttachMoney as MoneyIcon
} from '@mui/icons-material'
import { EstadisticasHoy, EstadisticasSemana, Cita } from '@/types/database'
import MetricCard from '@/components/MetricCard'
import CitasHoy from '@/components/CitasHoy'
import GraficoCitasSemana from '@/components/GraficoCitasSemana'
import GraficoServiciosPopulares from '@/components/GraficoServiciosPopulares'
import ProximasCitas from '@/components/ProximasCitas'
import BarberiaInfo from '@/components/BarberiaInfo'
import Notificaciones from '@/components/Notificaciones'

export default function Dashboard() {
  const [estadisticasHoy, setEstadisticasHoy] = useState<EstadisticasHoy | null>(null)
  const [estadisticasSemana, setEstadisticasSemana] = useState<EstadisticasSemana | null>(null)
  const [citasHoy, setCitasHoy] = useState<Cita[]>([])
  const [proximasCitas, setProximasCitas] = useState<Cita[]>([])
  const [loading, setLoading] = useState(true)
  const [lastUpdate, setLastUpdate] = useState(new Date())

  const fetchData = async () => {
    try {
      const [hoy, semana, citas, proximas] = await Promise.all([
        fetch('/api/estadisticas-hoy').then(res => res.json()),
        fetch('/api/estadisticas-semana').then(res => res.json()),
        fetch('/api/citas-hoy').then(res => res.json()),
        fetch('/api/proximas-citas').then(res => res.json())
      ])

      setEstadisticasHoy(hoy)
      setEstadisticasSemana(semana)
      setCitasHoy(citas)
      setProximasCitas(proximas)
      setLastUpdate(new Date())
    } catch (error) {
      console.error('Error fetching data:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 30000) // Actualizar cada 30 segundos
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <CircularProgress size={60} />
      </Box>
    )
  }

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
      <AppBar position="static" elevation={0} sx={{ bgcolor: 'background.paper', borderBottom: '1px solid #333' }}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 'bold' }}>
            Barbería Borges - Dashboard
          </Typography>
          <Chip 
            icon={<ScheduleIcon />} 
            label={`Última actualización: ${lastUpdate.toLocaleTimeString()}`}
            variant="outlined"
            size="small"
          />
          <IconButton onClick={fetchData} sx={{ ml: 1 }}>
            <RefreshIcon />
          </IconButton>
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ py: 4 }}>
        <Grid container spacing={3}>
          {/* Métricas principales */}
          <Grid item xs={12} md={3}>
            <MetricCard
              title="Citas Hoy"
              value={estadisticasHoy?.totalCitas || 0}
              icon={<ScheduleIcon />}
              color="primary"
              subtitle={`${estadisticasHoy?.citasCompletadas || 0} completadas`}
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <MetricCard
              title="Citas Pendientes"
              value={estadisticasHoy?.citasPendientes || 0}
              icon={<TrendingUpIcon />}
              color="warning"
              subtitle="Para hoy"
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <MetricCard
              title="Ingresos Estimados"
              value={`€${estadisticasHoy?.ingresosEstimados?.toFixed(2) || '0.00'}`}
              icon={<MoneyIcon />}
              color="success"
              subtitle="Para hoy"
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <MetricCard
              title="Barberos Activos"
              value={estadisticasHoy?.barberosActivos || 0}
              icon={<PeopleIcon />}
              color="info"
              subtitle="Disponibles"
            />
          </Grid>

          {/* Información de la barbería */}
          <Grid item xs={12} md={3}>
            <BarberiaInfo />
          </Grid>

          {/* Notificaciones */}
          <Grid item xs={12} md={3}>
            <Notificaciones />
          </Grid>

          {/* Citas de hoy */}
          <Grid item xs={12} md={6}>
            <CitasHoy citas={citasHoy} />
          </Grid>

          {/* Gráfico de citas por semana */}
          <Grid item xs={12} md={6}>
            <GraficoCitasSemana data={estadisticasSemana?.citasPorDia || []} />
          </Grid>

          {/* Gráfico de servicios populares */}
          <Grid item xs={12} md={6}>
            <GraficoServiciosPopulares data={estadisticasHoy?.serviciosPopulares || []} />
          </Grid>

          {/* Próximas citas */}
          <Grid item xs={12}>
            <ProximasCitas citas={proximasCitas} />
          </Grid>
        </Grid>
      </Container>
    </Box>
  )
}
