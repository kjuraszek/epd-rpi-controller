import { afterAll, beforeAll, describe, expect, it, vi } from 'vitest'
import { mount } from "@vue/test-utils"
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import AppFooter from "@/components/AppFooter.vue"


describe('AppFooter', () => {
  let vuetify = null
  let wrapper = null

  beforeAll(() => {
    vi.useFakeTimers()
    const mockedDate = new Date(2030, 1, 1, 13)
    vi.setSystemTime(mockedDate)
    vuetify = createVuetify({
      components,
      directives,
    })
    wrapper = mount({template: '<v-layout><AppFooter></AppFooter></v-layout>'}, {
      global: {
        plugins: [vuetify],
        components: {AppFooter}
      },
    })
  })

  afterAll(() => {
    vi.useRealTimers()
  })
  
  it("mounts properly", async () => {
    expect(AppFooter).toBeTruthy()
    expect(wrapper.find('.v-footer').exists()).toBe(true)
  })
  it("shows current year", async () => {
    expect(wrapper.text()).toContain("© 2030")
  })
})
