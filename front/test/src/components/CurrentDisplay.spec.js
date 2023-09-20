import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { nextTick } from 'vue'
import { mount, enableAutoUnmount } from "@vue/test-utils"
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { createTestingPinia  } from '@pinia/testing'
import CurrentDisplay from '@/components/CurrentDisplay.vue'
import { useUiStatusStore } from '@/stores/uiStatus'
import { useEpdStatusStore } from '@/stores/epdStatus'


global.fetch = vi.fn()

const vuetify = createVuetify({
  components,
  directives,
})

describe('CurrentDisplay', () => {

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
})
