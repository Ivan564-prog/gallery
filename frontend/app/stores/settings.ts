export const useRootSettingsStore = defineStore('rootSettings', () => {
    const settings = ref<IRootSettings>()
    const pageTitle = ref<string>('')

    const setRootSettings = async () => {
        const { data } = await useRequest<IRootSettings>('/api/v1/config/root/')
        settings.value = data.value
    }

    setRootSettings()
    return {
        setRootSettings,
        settings,
    }
})
