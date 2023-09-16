import { describe, expect, test, beforeAll, afterAll } from 'vitest'
import { HOST, API, STATUS_ENDPOINT, CURRENT_DISPLAY_ENDPOINT } from '@/consts'
import { mockWindowLocation, restoreWindowLocation, getMockedConsts } from 'test/helpers'


describe('Constants are properly set', () => {
    beforeAll(() => {
        mockWindowLocation()
    })
    
    afterAll(() => {
        restoreWindowLocation()
    })

    const mockedConsts = getMockedConsts()

    test('HOST properly set', async () => {
        expect(HOST).toBe(mockedConsts.HOST)
    })

    test('API properly set', async () => {
        expect(API).toBe(mockedConsts.API)
    })

    test('STATUS_ENDPOINT properly set', async () => {
        expect(STATUS_ENDPOINT).toBe(mockedConsts.STATUS_ENDPOINT)
    })
    test('CURRENT_DISPLAY_ENDPOINT properly set', async () => {
        expect(CURRENT_DISPLAY_ENDPOINT).toBe(mockedConsts.CURRENT_DISPLAY_ENDPOINT)
    })
})
