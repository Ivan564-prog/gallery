export const useRootSettingsStore = defineStore('rootSettings', () => {
    const settings = ref<IRootSettings>()
    const pageTitle = ref<string>('')

    const setRootSettings = async () => {
        const { data } = await useRequest<IRootSettings>('/api/v1/config/root/')
        settings.value = data.value
    }
    const setPT = (t: string) => {
        pageTitle.value = t
    }
    return {
        setRootSettings,
        pageTitle,
        settings,
        setPT,
    }
})
