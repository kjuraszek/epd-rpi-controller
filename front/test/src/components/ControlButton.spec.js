import { afterAll, beforeAll, afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { mount, enableAutoUnmount, flushPromises } from "@vue/test-utils"
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { createTestingPinia  } from '@pinia/testing'
import { mockWindowLocation, restoreWindowLocation } from 'test/helpers'
import ControlButton from '@/components/ControlButton.vue'
import { useUiStatusStore } from '@/stores/uiStatus'


global.fetch = vi.fn()

const vuetify = createVuetify({
  components,
  directives,
})

describe('ControlButton', () => {

  enableAutoUnmount(afterEach)

  beforeAll(() => {
    mockWindowLocation()
  })
  afterAll(() => {
    restoreWindowLocation()
  })

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
    })).toThrowError('Unknown action')
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
    })).toThrowError('Unknown action')
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

    expect(wrapper.getComponent('.v-icon').html()).toContain("mdi-arrow-right")
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

    expect(wrapper.getComponent('.v-icon').html()).toContain("mdi-arrow-left")
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
    wrapper.find('.v-btn').trigger('click')

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
