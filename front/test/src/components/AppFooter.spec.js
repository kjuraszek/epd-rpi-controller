import { afterAll, afterEach, beforeAll, beforeEach, describe, expect, it, vi } from 'vitest'
import { mount, enableAutoUnmount } from "@vue/test-utils"
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import AppFooter from "@/components/AppFooter.vue"


const vuetify = createVuetify({
  components,
  directives,
})

describe('AppFooter', () => {
  let wrapper = null
  enableAutoUnmount(afterEach)
  beforeAll(() => {
    vi.useFakeTimers()
    const mockedDate = new Date(2030, 1, 1, 13)
    vi.setSystemTime(mockedDate)
  })

  beforeEach(() => {
    wrapper = mount({template: '<v-layout><AppFooter></AppFooter></v-layout>'}, {
      props: {},
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
