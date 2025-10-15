export const useModalStore = defineStore('modals', () => {
    const openedModal = ref<string | null>(null)
    const optionalData = ref<TRequestBody>({})
    watch(openedModal, () => {
        document.body.style.overflow = openedModal.value ? 'hidden' : 'auto'
    })
    return {
        openedModal,
        optionalData,
    }
})
