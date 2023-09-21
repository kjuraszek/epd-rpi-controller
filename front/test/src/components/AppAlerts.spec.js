import { afterAll, afterEach, beforeAll, beforeEach, describe, expect, it, vi } from 'vitest'
import { nextTick } from 'vue'
import { mount } from "@vue/test-utils"
import { createTestingPinia  } from '@pinia/testing'
import { mockWindowLocation, restoreWindowLocation, vuetify } from 'test/helpers'
import AppAlerts from "@/components/AppAlerts.vue"
import { useUiStatusStore } from '@/stores/uiStatus'


describe('AppAlerts', () => {
  let wrapper = null
  let store = null

  beforeAll(() => {
    mockWindowLocation()
  })

  beforeEach(() => {
    wrapper = mount(AppAlerts, {
      global: {
        plugins: [vuetify,
          createTestingPinia({
            stubActions: false,
            createSpy: vi.fn
          })],
      },
    })

    store = useUiStatusStore()
  })

  afterEach(() => {
    document.body.outerHTML = ''
  })

  afterAll(() => {
    restoreWindowLocation()
  })

  it("mounts properly without alerts", async () => {
    expect(AppAlerts).toBeTruthy()

    expect(wrapper.exists()).toBe(true)
    expect(document.querySelector('.v-alert')).toBeNull()
  })
  it("shows success alert", async () => {
    store.$patch({successAlert: true, })
    
    await nextTick()

    expect(document.querySelector('.v-alert').textContent).toContain('View change has been triggered.')
    expect(document.getElementsByClassName('v-alert').length).toBe(1)
  })
  it("shows warning alert", async () => {
    store.$patch({warningAlert: true})
    
    await nextTick()
    expect(document.getElementsByClassName('v-alert').length).toBe(1)
    expect(document.querySelector('.v-alert').textContent).toContain('Warning - EPD is busy at this moment')
    expect(document.getElementsByClassName('v-alert').length).toBe(1)
  })
  it("shows error alert", async () => {
    store.$patch({errorAlert: true})
    
    await nextTick()

    expect(document.querySelector('.v-alert').textContent).toContain('Action failed - unable to connect to')
    expect(document.getElementsByClassName('v-alert').length).toBe(1)
  })
  it("shows error alert with last succesful check", async () => {
    const mockedDate = "2023-09-10, 21:51:14"
    store.$patch({
      errorAlert: true,
      lastSuccessfulCheck: mockedDate
    })
    
    await nextTick()

    expect(document.querySelector('.v-alert').textContent).toContain('Action failed - unable to connect to')
    expect(document.querySelector('.v-alert').textContent).toContain('2023-09-10, 21:51:14')
    expect(document.getElementsByClassName('v-alert').length).toBe(1)
  })
})
