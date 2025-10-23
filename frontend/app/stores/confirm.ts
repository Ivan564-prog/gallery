export const useConfirmStore = defineStore('confirm', () => {
    const modalStore = useModalStore()

    const resolvePromise = ref<((value: any) => void) | null>(null)
    const rejectPromise = ref<((value: any) => void) | null>(null)

    const titleWindow = ref<string>('')
    const textWindow = ref<string>('')

    const openConfirmModal = (title: string, text: string) => {
        titleWindow.value = title
        textWindow.value = text
        modalStore.openedModal = 'confirm'

        return new Promise((resolve, reject) => {
            resolvePromise.value = resolve
            rejectPromise.value = reject            
        })
    }

    const confirm = (data: any) => {
        if (resolvePromise.value) {
            resolvePromise.value(data)
            clear()
        }
        modalStore.openedModal = null
    }

    const cancel = (data: any) => {
        if (rejectPromise.value) {
            rejectPromise.value(data)
            clear()
        }
        modalStore.openedModal = null
    }

    const clear = () => {
        resolvePromise.value = null
        rejectPromise.value = null
    }

    return {
        openConfirmModal,
        titleWindow,
        textWindow,
        confirm,
        cancel,
    }
})