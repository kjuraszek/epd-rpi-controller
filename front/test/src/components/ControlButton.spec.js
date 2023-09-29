import { afterEach, beforeEach, describe, expect, it, vi } from "vitest"
import { mount, enableAutoUnmount, flushPromises } from "@vue/test-utils"
import { createTestingPinia  } from "@pinia/testing"
import ControlButton from "@/components/ControlButton.vue"
import { useUiStatusStore } from "@/stores/uiStatus"
import { vuetify } from "test/helpers"


global.fetch = vi.fn()


describe("ControlButton", () => {

  enableAutoUnmount(afterEach)


  it("throws error when no action set", async () => {
    expect( () => mount(ControlButton, {
      props: {},
      global: {
      plugins: [vuetify,
        createTestingPinia({
          stubActions: false,
          createSpy: vi.fn
        })],
      },
    })).toThrowError("Unknown action")
  })
  it("throws error when unknown action set", async () => {
    expect( () => mount(ControlButton, {
      props: {
        controlAction: "test"
      },
      global: {
      plugins: [vuetify,
        createTestingPinia({
          stubActions: false,
          createSpy: vi.fn
        })],
      },
    })).toThrowError("Unknown action")
  })
  it("mounts properly next button", async () => {
    const wrapper = mount(ControlButton, {
      props: {
        controlAction: "next"
      },
      global: {
        plugins: [vuetify,
          createTestingPinia({
          stubActions: false,
          createSpy: vi.fn
        })],
      },
    })

    expect(wrapper.getComponent(".v-icon").html()).toContain("mdi-arrow-right")
  })
  it("mounts properly prev button", async () => {
    const wrapper = mount(ControlButton, {
      props: {
        controlAction: "prev"
      },
      global: {
        plugins: [vuetify,
          createTestingPinia({
            stubActions: false,
            createSpy: vi.fn
          })
        ],
      },
    })

    expect(wrapper.getComponent(".v-icon").html()).toContain("mdi-arrow-left")
  })
  it("triggers switchView on button click", async () => {
    const wrapper = mount(ControlButton, {
      props: {
        controlAction: "prev"
      },
      global: {
        plugins: [vuetify,
          createTestingPinia({
            stubActions: false,
            createSpy: vi.fn
          })
        ],
      },
    })
    vi.spyOn(wrapper.vm, "switchView").mockImplementation(vi.fn)
    wrapper.find(".v-btn").trigger("click")

    expect(wrapper.vm.switchView).toHaveBeenCalledTimes(1)
  })
  describe("methods", () => {
    describe("switchView", () => {
      let wrapper = null
      let store = null
      beforeEach(() => {
        wrapper = mount(ControlButton, {
          props: {
            controlAction: "next"
          },
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
      it("switches view with success", async () => {
        const response = {
          status: 204
        }

        fetch.mockResolvedValue(response)
        vi.spyOn(store, "resetAlerts")
        expect(store.successAlert).toBe(false)

        wrapper.vm.switchView()

        await flushPromises()

        expect(store.resetAlerts).toHaveBeenCalledTimes(1)
        expect(store.successAlert).toBe(true)
      })
      it("switching view fails with warning", async () => {
        const response = {
          status: 404
        }

        fetch.mockResolvedValue(response)
        vi.spyOn(store, "resetAlerts")
        expect(store.warningAlert).toBe(false)

        wrapper.vm.switchView()

        await flushPromises()

        expect(store.resetAlerts).toHaveBeenCalledTimes(1)
        expect(store.warningAlert).toBe(true)
      })
      it("switching view fails with error", async () => {
        const response = {
          status: 500
        }

        fetch.mockResolvedValue(response)
        vi.spyOn(store, "resetAlerts")
        expect(store.errorAlert).toBe(false)

        wrapper.vm.switchView()

        await flushPromises()

        expect(store.resetAlerts).toHaveBeenCalledTimes(1)
        expect(store.errorAlert).toBe(true)
      })
      it("fetching UI status fails", async () => {
        const response = null

        fetch.mockResolvedValue(response)
        vi.spyOn(store, "resetAlerts")
        expect(store.errorAlert).toBe(false)

        wrapper.vm.switchView()

        await flushPromises()

        expect(store.resetAlerts).toHaveBeenCalledTimes(1)
        expect(store.errorAlert).toBe(true)
      })
    })
  })
})
