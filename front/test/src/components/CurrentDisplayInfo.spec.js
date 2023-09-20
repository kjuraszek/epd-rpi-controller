import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { nextTick } from 'vue'
import { mount, enableAutoUnmount } from "@vue/test-utils"
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { createTestingPinia  } from '@pinia/testing'
import CurrentDisplayInfo from '@/components/CurrentDisplayInfo.vue'
import { useEpdStatusStore } from '@/stores/epdStatus'


global.fetch = vi.fn()

const vuetify = createVuetify({
  components,
  directives,
})

describe('CurrentDisplayInfo', () => {

    enableAutoUnmount(afterEach)

    let wrapper = null
    let epdStatusStore = null
    beforeEach(() => {
        wrapper = mount(CurrentDisplayInfo, {
            global: {
                plugins: [vuetify,
                createTestingPinia({
                    stubActions: false,
                    createSpy: vi.fn
                })],
            },
        })

        epdStatusStore = useEpdStatusStore()
    })
    it("mounts properly", async () => {
        expect(CurrentDisplayInfo).toBeTruthy()
        expect(wrapper.exists()).toBe(true)
    })
    it("shows nothing if currentView and totalViews not set", async () => {
        expect(wrapper.find("p").exists()).toBe(false)
    })
    it("shows info when views data set", async () => {
        epdStatusStore.$patch({
            currentView: 1,
            totalViews: 5,
        })
        await nextTick()
        console.log(wrapper.html())
        expect(wrapper.findAll("p").length).toBe(2)
        expect(wrapper.findAll("p")[0].text().length).toBe(0)
        expect(wrapper.findAll("p")[1].text()).toContain("View 2 of 5")
    })
    it("shows info when views data set and when EPD busy", async () => {
        epdStatusStore.$patch({
            currentView: 1,
            totalViews: 5,
            epdBusy: true,
        })
        await nextTick()
        console.log(wrapper.html())
        expect(wrapper.findAll("p").length).toBe(2)
        expect(wrapper.findAll("p")[0].text()).toContain("(EPD is switching)")
        expect(wrapper.findAll("p")[1].text()).toContain("View 2 of 5")
    })
    // it("shows image with shadow when loading", async () => {
    //     epdStatusStore.currentImage = "http://localhost/image.jpg"
    //     await nextTick()

    //     expect(wrapper.find("div.img-loading-shadow").exists()).toBe(true)
    //     expect(wrapper.find("img").exists()).toBe(true)
    // })
})
