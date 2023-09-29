import { beforeEach, describe, expect, it } from "vitest"
import { useUiStatusStore } from "@/stores/uiStatus"
import { createPinia, setActivePinia } from "pinia"

describe("uiStatus Store", () => {
    beforeEach(() => {
        setActivePinia(createPinia())
      })
    describe("actions", () => {
        describe("resetAlerts", () => {
            it("resets all alerts", async () => {
              const store = useUiStatusStore(createPinia())
              store.successAlert = true
              store.warningAlert = true
              store.errorAlert = true

              store.resetAlerts()
              expect(store.successAlert).toBe(false)
              expect(store.warningAlert).toBe(false)
              expect(store.errorAlert).toBe(false)
            })
          })
    })
})