// Popup finto: imita l'integrazione con il gestionale (nei test non viene mai eseguito un invio).
export default function BookingPopup() {
  const invia = () => fetch('/api/richieste', { method: 'POST' })
  return <button onClick={invia}>Prenota</button>
}
