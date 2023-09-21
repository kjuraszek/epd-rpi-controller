import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'


const vuetify = createVuetify({
  components,
  directives,
})

const GLOBAL_LOCATION = global.window.location

const mockWindowLocation = () => {
    delete global.window.location
    global.window = Object.create(window)
    global.window.location = {
        hostname: 'localhost',
        protocol: 'http'
    }
}

const restoreWindowLocation = () => {
    delete global.window.location;
    global.window = Object.create(window)
    global.window.location = GLOBAL_LOCATION
}

const getMockedConsts = () => ({ 
    HOST: 'http://localhost',
    API: 'http://localhost:50000/api',
    STATUS_ENDPOINT: 'http://localhost:50000/api/status',
    CURRENT_DISPLAY_ENDPOINT: 'http://localhost:50000/api/current_display'
})


const createFetchResponseJSON = (data) => {
    return { json: () => new Promise((resolve) => resolve(data)) }
}
  
const createFetchResponseBlob = (data) => {
    return { blob: () => new Promise((resolve) => resolve(data)) }
}

export { mockWindowLocation, restoreWindowLocation, getMockedConsts, createFetchResponseJSON, createFetchResponseBlob, vuetify }
