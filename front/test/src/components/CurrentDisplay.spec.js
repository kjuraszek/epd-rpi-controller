import { afterEach, beforeEach, describe, expect, it, vi } from "vitest"
import { nextTick } from "vue"
import { mount, enableAutoUnmount, flushPromises } from "@vue/test-utils"
import { createTestingPinia  } from "@pinia/testing"
import CurrentDisplay from "@/components/CurrentDisplay.vue"
import { useUiStatusStore } from "@/stores/uiStatus"
import { useEpdStatusStore } from "@/stores/epdStatus"
import { vuetify } from "test/helpers"


global.fetch = vi.fn()


describe("CurrentDisplay", () => {

  enableAutoUnmount(afterEach)

  let wrapper = null
  let uiStatusStore = null
  let epdStatusStore = null
  beforeEach(() => {
    wrapper = mount(CurrentDisplay, {
      global: {
        plugins: [vuetify,
        createTestingPinia({
          stubActions: false,
          createSpy: vi.fn
        })],
      },
    })

    uiStatusStore = useUiStatusStore()
    epdStatusStore = useEpdStatusStore()
  })
  it("mounts properly", async () => {
    expect(CurrentDisplay).toBeTruthy()
    expect(wrapper.exists()).toBe(true)
  })
  it("shows info when no image set", async () => {
    expect(wrapper.find("img").exists()).toBe(false)
    expect(wrapper.find("p").text()).toContain("Unable to load an image")
  })
  it("shows image when set", async () => {
    epdStatusStore.currentImage = "http://localhost/image.jpg"
    await nextTick()

    expect(wrapper.find("div.img-no-shadow").exists()).toBe(true)
    expect(wrapper.find("img").exists()).toBe(true)
  })
  it("shows image with shadow when loading", async () => {
    epdStatusStore.currentImage = "http://localhost/image.jpg"
    uiStatusStore.loadingImage = true
    await nextTick()

    expect(wrapper.find("div.img-loading-shadow").exists()).toBe(true)
    expect(wrapper.find("img").exists()).toBe(true)
  })
  it("triggers swipeHandler on horizontal swipe", async () => {
    const response = {
      status: 204
    }
    fetch.mockResolvedValue(response)
    epdStatusStore.currentImage = "http://localhost/image.jpg"

    await nextTick()

    const spy = vi.spyOn(wrapper.vm, "swipeHandler")
    wrapper.find("div.img-no-shadow").trigger("touchstart", { changedTouches:[
      {
        clientX: 199,
        clientY: 451,
        identifier: 99
      }
    ] })
    wrapper.find("div.img-no-shadow").trigger("touchend", { changedTouches:[
      {
        clientX: 23,
        clientY: 451,
        identifier: 99
      }
    ] })
    await nextTick()

    expect(spy).toHaveBeenCalledWith("prev")
  })
  it("does nothing on vertical swipe", async () => {
    const response = {
      status: 204
    }
    fetch.mockResolvedValue(response)
    epdStatusStore.currentImage = "http://localhost/image.jpg"

    await nextTick()

    const spy = vi.spyOn(wrapper.vm, "swipeHandler")
    wrapper.find("div.img-no-shadow").trigger("touchstart", { changedTouches:[
      {
        clientX: 199,
        clientY: 451,
        identifier: 99
      }
    ] })
    wrapper.find("div.img-no-shadow").trigger("touchend", { changedTouches:[
      {
        clientX: 199,
        clientY: 251,
        identifier: 99
      }
    ] })
    await nextTick()

    expect(spy).toHaveBeenCalledTimes(0)
  })
  describe("methods", () => {
    describe("swipeHandler", () => {
      it("switches view with success", async () => {
        const response = {
          status: 204
        }

        fetch.mockResolvedValue(response)
        vi.spyOn(uiStatusStore, "resetAlerts")
        expect(uiStatusStore.successAlert).toBe(false)

        wrapper.vm.swipeHandler()

        await flushPromises()

        expect(uiStatusStore.resetAlerts).toHaveBeenCalledTimes(1)
        expect(uiStatusStore.successAlert).toBe(true)
      })
      it("switching view fails with warning", async () => {
        const response = {
          status: 404
        }

        fetch.mockResolvedValue(response)
        vi.spyOn(uiStatusStore, "resetAlerts")
        expect(uiStatusStore.warningAlert).toBe(false)

        wrapper.vm.swipeHandler()

        await flushPromises()

        expect(uiStatusStore.resetAlerts).toHaveBeenCalledTimes(1)
        expect(uiStatusStore.warningAlert).toBe(true)
      })
      it("switching view fails with error", async () => {
        const response = {
          status: 500
        }

        fetch.mockResolvedValue(response)
        vi.spyOn(uiStatusStore, "resetAlerts")
        expect(uiStatusStore.errorAlert).toBe(false)

        wrapper.vm.swipeHandler()

        await flushPromises()

        expect(uiStatusStore.resetAlerts).toHaveBeenCalledTimes(1)
        expect(uiStatusStore.errorAlert).toBe(true)
      })
      it("fetching UI status fails", async () => {
        const response = null

        fetch.mockResolvedValue(response)
        vi.spyOn(uiStatusStore, "resetAlerts")
        expect(uiStatusStore.errorAlert).toBe(false)

        wrapper.vm.swipeHandler()

        await flushPromises()

        expect(uiStatusStore.resetAlerts).toHaveBeenCalledTimes(1)
        expect(uiStatusStore.errorAlert).toBe(true)
      })
    })
  })
})
