export default defineNuxtRouteMiddleware(async to => {
    const userStore = useUserStore()

    if (to.meta.public)
        return

    if (!userStore.userData)
        await userStore.setUserData()

    if (!userStore.userData)
        return navigateTo('/login')
})