export const useCartStore = defineStore('cart', () => {
    const cart = ref<ICart>()

    const setCart = async () => {
        const { data } = await useRequest<ICart>('/api/v1/cart/')
        cart.value = data.value
    }

    const createCartItem = async (productId: number, quantity: number) => {
        try {
            const { data } = await useRequest<ICart>('/api/v1/cart/', 'POST', {
                product_id: productId,
                quantity: quantity,
            })
            cart.value = data.value
        } catch {}
    }

    const updateCartItem = async (positionId: number, quantity: number) => {
        try {
            const { data } = await useRequest<ICart>(`/api/v1/cart/${positionId}/`, 'PATCH', {
                quantity: quantity,
            })
            cart.value = data.value
        } catch {}
    }

    const deleteCartItem = async (positionId: number) => {
        try {
            const { data } = await useRequest<ICart>(`/api/v1/cart/${positionId}/`, 'DELETE')
            cart.value = data.value
        } catch {}
    }

    return {
        cart,
        setCart,
        createCartItem,
        updateCartItem,
        deleteCartItem,
    }
})
