// @vitest-environment jsdom
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import HitTable from '../HitTable.vue'

describe('HitTable.vue', () => {
  beforeEach(() => {
    vi.resetAllMocks()
  })

  it('renders table with hits', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => [
        { route: '/', count: 10 },
        { route: '/about', count: 5 }
      ]
    })
    const wrapper = mount(HitTable)
    await new Promise(r => setTimeout(r, 0))
    expect(wrapper.text()).toContain('Route Hit Counts')
    expect(wrapper.text()).toContain('/')
    expect(wrapper.text()).toContain('10')
    expect(wrapper.text()).toContain('/about')
    expect(wrapper.text()).toContain('5')
    expect(wrapper.findAll('tbody tr').length).toBe(2)
  })

  it('shows loading when no hits', async () => {
    global.fetch = vi.fn().mockResolvedValue({ ok: true, json: async () => [] })
    const wrapper = mount(HitTable)
    await new Promise(r => setTimeout(r, 0))
    expect(wrapper.text()).toContain('Loading...')
  })

  it('shows loading when fetch fails', async () => {
    global.fetch = vi.fn().mockRejectedValue(new Error('fail'))
    const wrapper = mount(HitTable)
    await new Promise(r => setTimeout(r, 0))
    expect(wrapper.text()).toContain('Loading...')
  })
}) 