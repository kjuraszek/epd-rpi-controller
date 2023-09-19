import { afterAll, beforeAll, beforeEach, describe, expect, it, vi } from 'vitest'
import { nextTick } from 'vue'
import { mount } from "@vue/test-utils"
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { createTestingPinia  } from '@pinia/testing'
import { mockWindowLocation, restoreWindowLocation } from 'test/helpers'
import AppMain from "@/components/AppMain.vue"
import ControlButton from '@/components/ControlButton.vue'
import CurrentDisplay from '@/components/CurrentDisplay.vue'
import MainHeadings from '@/components/MainHeadings.vue'
import { useUiStatusStore } from '@/stores/uiStatus'


const vuetify = createVuetify({
  components,
  directives,
})

describe('AppMain', () => {
  let wrapper = null
  let store = null

  beforeAll(() => {
    mockWindowLocation()
  })

  beforeEach(() => {
    wrapper = mount(AppMain, {
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

  afterAll(() => {
    restoreWindowLocation()
  })

  it("mounts properly", async () => {

    expect(AppMain).toBeTruthy()
    expect(wrapper.exists()).toBe(true)
  })
  it("has proper components", async () => {

    expect(wrapper.findAllComponents(MainHeadings)).toHaveLength(1)
    expect(wrapper.findAllComponents(ControlButton)).toHaveLength(2)
    expect(wrapper.findAllComponents(CurrentDisplay)).toHaveLength(1)
    expect(wrapper.findComponent('.v-alert').exists()).toBe(false)
  })
  it("shows error alert when more than 50 failed requests", async () => {
    store.$patch({
        failedRequestsCount: 51,
    })
    
    await nextTick()

    expect(wrapper.findAllComponents(MainHeadings)).toHaveLength(1)
    expect(wrapper.findComponent(ControlButton).exists()).toBe(false)
    expect(wrapper.findComponent(CurrentDisplay).exists()).toBe(false)
    expect(wrapper.getComponent('.v-alert').text()).toContain('Unable to connect to an API')
  })
})
