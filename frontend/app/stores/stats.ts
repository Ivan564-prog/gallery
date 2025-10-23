export const useStatsStore = defineStore('stats', () => {
    const stats = ref<IStats>()

    const setStats = async () => {
        stats.value = await request<IStats>('/api/v1/config/stats/')
    }
    setStats()

    return {
        stats,
        setStats,
    }
})