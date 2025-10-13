export const useUserStore = defineStore('userStore', () => {
    const userData = ref<IUser | null>(null)

    const setUserData = async () => {
        const { data } = await useRequest<IUser | null>('/api/v1/user/')
        userData.value = data.value
    }
    setUserData()
    return {
        userData,
    }
})
