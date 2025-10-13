export const useDomainStore = defineStore('domain', () => {
    const domains = ref<IDomain[]>([])
    const domainSlug = ref<string>('')
    const setDomains = async () => {
        domains.value = await $fetch<IDomain[]>(`${getAPIUrl()}/api/v1/config/domain/`)
        // domains.value = data.value
    }
    const hasDomain = (slug: string) => {
        if (!domains.value.length) return !slug
        else return !!domains.value.filter(item => item.slug == slug).length
    }
    const activeDomain = () => {
        return domains.value.filter(item => item.slug == domainSlug.value)[0]
    }
    return {
        domains,
        domainSlug,
        hasDomain,
        activeDomain,
        setDomains,
    }
})
