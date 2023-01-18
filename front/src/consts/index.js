const VITE_API_PORT = import.meta.env.VITE_API_PORT

const HOST = `${window.location.protocol}//${window.location.hostname}`
const API = `${HOST}:${VITE_API_PORT}/api`
const STATUS_ENDPOINT = `${API}/status`
const CURRENT_DISPLAY_ENDPOINT = `${API}/current_display`

export { HOST, API, STATUS_ENDPOINT, CURRENT_DISPLAY_ENDPOINT }
