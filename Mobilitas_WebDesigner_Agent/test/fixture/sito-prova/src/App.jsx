import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Reflusso from './pages/Reflusso'

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/reflusso" element={<Layout hideWhatsApp><Reflusso /></Layout>} />
      </Routes>
    </Router>
  )
}
