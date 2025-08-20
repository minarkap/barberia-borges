import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Barbería Borges - Dashboard',
  description: 'Panel de control en tiempo real para la Barbería Borges',
}

const theme = createTheme()

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="es">
      <body className={inter.className}>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
