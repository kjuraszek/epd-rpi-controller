import { nextTick } from "vue"
import { afterAll, afterEach, beforeAll, beforeEach, describe, expect, it, vi } from "vitest"
import { mount, flushPromises } from "@vue/test-utils"
import { createTestingPinia  } from "@pinia/testing"
import { mockWindowLocation, restoreWindowLocation, vuetify } from "test/helpers"
import App from "@/App.vue"
import { useUiStatusStore } from "@/stores/uiStatus"


describe("App", () => {
  let wrapper = null
  let app = null
  let store = null

  beforeAll(() => {
    mockWindowLocation()
  })

  beforeEach(() => {
    wrapper = mount({template: "<v-layout><App></App></v-layout>"}, {
      props: {},
      global: {
        plugins: [vuetify,
          createTestingPinia({
            createSpy: vi.fn
          })],
        components: {App}
      },
    })
    app = wrapper.getComponent(App)
    store = useUiStatusStore()
  })

  afterAll(() => {
    restoreWindowLocation()
  })

  it("mounts properly and sets interval", async () => {
    expect(App).toBeTruthy()

    expect(app.exists()).toBe(true)
    expect(app.vm.$data.interval).not.toBe(null)
  })
  it("has proper components", async () => {
    expect(app.findAllComponents(".v-toolbar").length).toBe(1)
    expect(app.findAllComponents(".v-main").length).toBe(1)
    expect(app.findAllComponents(".v-footer").length).toBe(1)
  })
  describe("methods", () => {
    describe("startInterval", () => {
      beforeEach(() => {
        vi.useFakeTimers()
        wrapper = mount({template: "<v-layout><App></App></v-layout>"}, {
          props: {},
          global: {
            plugins: [vuetify,
              createTestingPinia({
                createSpy: vi.fn
              })],
            components: {App}
          },
        })
        app = wrapper.getComponent(App)
      })
    
      afterEach(() => {
        vi.useRealTimers()
      })
      it("starts interval and calls fetchStatus", async () => {
        const spyFetchStatus = vi.spyOn(app.vm, "fetchStatus").mockImplementation(vi.fn)

        vi.advanceTimersByTime(1205)

        expect(spyFetchStatus).toBeCalledTimes(2)
      })
    })
  })
  describe("watchers", () => {
    describe("failedRequestsCount", () => {
      it("stops interval after 50 of failed requests", async () => {
        vi.spyOn(global, "clearInterval")
        store.failedRequestsCount = 51

        await nextTick()
        flushPromises()

        expect(clearInterval).toBeCalledTimes(1)
      })
    })
  })
  describe("unmounts", () => {
    it("clears interval on unmount", async () => {
      const spy = vi.spyOn(global, "clearInterval")
      wrapper.unmount()

      await nextTick()
      flushPromises()

      expect(spy).toBeCalledTimes(1)
    })
  })
})
