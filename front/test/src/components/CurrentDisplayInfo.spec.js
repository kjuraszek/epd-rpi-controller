import { nextTick } from 'vue'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { mount, enableAutoUnmount } from "@vue/test-utils"
import { createTestingPinia  } from '@pinia/testing'
import CurrentDisplayInfo from '@/components/CurrentDisplayInfo.vue'
import { useEpdStatusStore } from '@/stores/epdStatus'
import { vuetify } from 'test/helpers'


global.fetch = vi.fn()


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

        expect(wrapper.findAll("p").length).toBe(2)
        expect(wrapper.findAll("p")[0].text()).toContain("(EPD is switching)")
        expect(wrapper.findAll("p")[1].text()).toContain("View 2 of 5")
    })
})
