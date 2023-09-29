import { afterAll, afterEach, beforeAll, beforeEach, describe, expect, it, vi } from "vitest"
import { mount, enableAutoUnmount } from "@vue/test-utils"
import AppFooter from "@/components/AppFooter.vue"
import { vuetify } from "test/helpers"


describe("AppFooter", () => {
  let wrapper = null
  enableAutoUnmount(afterEach)
  beforeAll(() => {
    vi.useFakeTimers()
    const mockedDate = new Date(2030, 1, 1, 13)
    vi.setSystemTime(mockedDate)
  })

  beforeEach(() => {
    wrapper = mount({template: "<v-layout><AppFooter></AppFooter></v-layout>"}, {
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
    expect(wrapper.find(".v-footer").exists()).toBe(true)
  })
  it("shows current year", async () => {
    expect(wrapper.text()).toContain("© 2030")
  })
})
