import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { flushPromises } from "@vue/test-utils";
import { createPinia, setActivePinia } from 'pinia'
import { useEpdStatusStore } from '@/stores/epdStatus'
import { useUiStatusStore } from '@/stores/uiStatus'
import { createFetchResponseJSON, createFetchResponseBlob } from 'test/helpers'


global.fetch = vi.fn()
global.URL.createObjectURL = vi.fn()

describe('epdStatus Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })
  afterEach(() => {
    vi.clearAllMocks()
    vi.resetAllMocks()
  })
  describe('actions', () => {
      describe('fetchStatus', () => {
        it('is triggering fetching image and updating epdStatus', async () => {
          
          const epdResponse = {
            "current_view": 0,
            "epd_busy": false,
            "total_views": 0,
            "timestamp": "2023-09-10, 21:51:14"
          }

          fetch.mockResolvedValue(createFetchResponseJSON(epdResponse))

          const epdStatusStore = useEpdStatusStore()
          const uiStatusStore = useUiStatusStore()
          const spyFetchCurrentImage = vi.spyOn(epdStatusStore, 'fetchCurrentImage').mockImplementation(vi.fn)
          const spyPatch = vi.spyOn(uiStatusStore, '$patch').mockImplementation()

          expect(epdStatusStore.timestamp).toBe(null)

          await epdStatusStore.fetchStatus()
          await flushPromises()

          expect(epdStatusStore.timestamp).toBe("2023-09-10, 21:51:14")
          expect(uiStatusStore.fetchingStatus).toBe(false)
          expect(spyFetchCurrentImage).toHaveBeenCalledOnce()
          expect(spyPatch).toHaveBeenCalledTimes(4)
        })

        it('is not fetching image if epd is busy', async () => {
          
          const epdResponse = {
            "current_view": 0,
            "epd_busy": true,
            "total_views": 0,
            "timestamp": "2023-09-10, 21:51:14"
          }

          fetch.mockResolvedValue(createFetchResponseJSON(epdResponse))

          const epdStatusStore = useEpdStatusStore()
          const uiStatusStore = useUiStatusStore()
          const spyFetchCurrentImage = vi.spyOn(epdStatusStore, 'fetchCurrentImage').mockImplementation(vi.fn)
          const spyPatch = vi.spyOn(uiStatusStore, '$patch').mockImplementation()

          await epdStatusStore.fetchStatus()
          await flushPromises()

          expect(uiStatusStore.fetchingStatus).toBe(false)
          expect(spyFetchCurrentImage).not.toHaveBeenCalled()
          expect(spyPatch).toHaveBeenCalledTimes(2)
        })

        it('updates UI status when fetching status fails', async () => {

          const epdResponse = null

          fetch.mockResolvedValue(createFetchResponseJSON(epdResponse))

          const epdStatusStore = useEpdStatusStore()
          const uiStatusStore = useUiStatusStore()
          const spyFetchCurrentImage = vi.spyOn(epdStatusStore, 'fetchCurrentImage').mockImplementation(vi.fn)
          const spyPatch = vi.spyOn(uiStatusStore, '$patch')

          await epdStatusStore.fetchStatus()
          await flushPromises()

          expect(uiStatusStore.errorAlert).toBe(true)
          expect(uiStatusStore.successAlert).toBe(false)
          expect(uiStatusStore.warningAlert).toBe(false)
          expect(uiStatusStore.failedRequestsCount).toBe(1)
          expect(spyFetchCurrentImage).not.toHaveBeenCalled()
          expect(spyPatch).toHaveBeenCalledTimes(3)
        })

        it('not fetching image if UI is already fetching', async () => {

          const epdStatusStore = useEpdStatusStore()
          const uiStatusStore = useUiStatusStore()
          uiStatusStore.$patch({fetchingStatus: true})

          const spyFetchCurrentImage = vi.spyOn(epdStatusStore, 'fetchCurrentImage').mockImplementation(vi.fn)
          const spyPatch = vi.spyOn(uiStatusStore, '$patch').mockImplementation()


          await epdStatusStore.fetchStatus()
          await flushPromises()

          expect(spyFetchCurrentImage).not.toHaveBeenCalled()
          expect(spyPatch).not.toHaveBeenCalled()
        })
      })
      describe('fetchCurrentImage', () => {
        it('is fetching image and updating epdStatus', async () => {
          
          const epdResponse = new Blob(['1,2,3'], {type: 'image/jpg'})
          const mockedObjectURL = "blob:localhost/1e423fda-22a2-4b2a-bca9-ab5c186493fe"

          fetch.mockResolvedValue(createFetchResponseBlob(epdResponse))
          URL.createObjectURL.mockImplementation(() => mockedObjectURL)

          const epdStatusStore = useEpdStatusStore()
          const uiStatusStore = useUiStatusStore()
          const spyPatch = vi.spyOn(uiStatusStore, '$patch')

          await epdStatusStore.fetchCurrentImage()
          await flushPromises()

          expect(epdStatusStore.currentImage).toBe(mockedObjectURL)
          expect(uiStatusStore.loadingImage).toBe(false)
          expect(spyPatch).toHaveBeenCalledTimes(1)
        })
        it('updates UI status when fetching image fails', async () => {

          const epdResponse = null

          fetch.mockResolvedValue(createFetchResponseJSON(epdResponse))

          const epdStatusStore = useEpdStatusStore()
          const uiStatusStore = useUiStatusStore()
          const spyPatch = vi.spyOn(uiStatusStore, '$patch')

          await epdStatusStore.fetchCurrentImage()
          await flushPromises()

          expect(uiStatusStore.errorAlert).toBe(true)
          expect(uiStatusStore.successAlert).toBe(false)
          expect(uiStatusStore.warningAlert).toBe(false)
          expect(spyPatch).toHaveBeenCalledTimes(1)
        })
      })
  })
})