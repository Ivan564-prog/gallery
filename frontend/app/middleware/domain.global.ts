export default defineNuxtRouteMiddleware(to => {
    const domainStore = useDomainStore()

    domainStore.setDomains().then(() => {
        if (!domainStore.hasDomain(<string>to.params.domain)) {
            if (to.params.page) throw createError('404')
            else {
                to.params.page = to.params.heading
                to.params.heading = to.params.domain
                to.params.domain = ''
            }
        }
        domainStore.domainSlug = <string>to.params.domain ? <string>to.params.domain : ''
    })
})
