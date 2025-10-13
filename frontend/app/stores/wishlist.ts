export const useWishlistStore = defineStore('wishlistStore', () => {
    const wishlist = ref<number[]>([])

    const setWishlist = async () => {
        const { data } = await useRequest<number[]>('/api/v1/wishlist/')
        wishlist.value = data.value
    }

    const getDetailWishlist = async () => {
        const { data } = await useRequest<IProduct[]>('/api/v1/wishlist/products/')
        return data.value
    }

    const toggleWishlistItem = async (productId: number) => {
        const { data } = await useRequest<number[]>('/api/v1/wishlist/', 'POST', {
            productId: productId,
        })
        wishlist.value = data.value
    }

    return {
        wishlist,
        setWishlist,
        toggleWishlistItem,
        getDetailWishlist,
    }
})
