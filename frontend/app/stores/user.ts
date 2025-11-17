export const useUserStore = defineStore('userStore', () => {
    const userData = ref<IUser | null>(null)

    const setUserData = async () => {
        const userID = useCookie('user-id')
        if (!userID.value) return

        const { data } = await useRequest<IUser | null>(`/api/v1/user/${userID.value}/`)
        userData.value = data.value
    }
    return {
        userData,
        setUserData,
    }
})
