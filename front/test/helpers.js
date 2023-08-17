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


export { mockWindowLocation, restoreWindowLocation, getMockedConsts }