type TMethod = 'GET' | 'PATCH' | 'POST' | 'PUT' | 'DELETE'

export const getAPIUrl = () => {
    const runtimeConfig = useRuntimeConfig()
    return `${useRequestURL().protocol}//localhost:8000`
}
let csrf: string

export const useRequest = async <T>(url: string, method?: TMethod, body?: TRequestBody) => {
    url = getAPIUrl() + url
    const response = await useFetch(url, {
        method,
        [method == 'GET' ? 'params' : 'body']: body,
        headers: {
            ...useRequestHeaders(['cookie']),
        },
        credentials: 'include',
    })

    if (response.error.value) throw createError(response.error.value)
    return {
        error: response.error,
        data: response.data as Ref<T>,
        refresh: response.refresh,
        status: response.status,
    }
}

export const request = async <T>(url: string, method?: TMethod, body?: TRequestBody) => {
    url = getAPIUrl() + url
    try {
        const response = await $fetch<T>(url, {
            method,
            credentials: 'include',
            [method == 'GET' ? 'params' : 'body']: body,
            headers: {
                ...useRequestHeaders(['cookie']),
            },
        })
        return response
    } catch (error: any) {
        throw createError(error)
    }
}
