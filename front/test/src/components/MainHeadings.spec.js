import { describe, expect, it } from 'vitest'
import {mount} from "@vue/test-utils"
import MainHeadings from "@/components/MainHeadings.vue"


describe('MainHeadings', () => {
  it("mounts properly", async () => {
    expect(MainHeadings).toBeTruthy()
    const wrapper = mount(MainHeadings)

    expect(wrapper.find('h1').exists()).toBe(true)
    expect(wrapper.find('p').exists()).toBe(true)
  })
})
