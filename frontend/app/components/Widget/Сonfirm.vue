<script lang="ts" setup>
    const MODAL_NAME = 'reset-password-success'
    defineProps<{
        title?: string
        text?: string
    }>()
    const modalStore = useModalStore()
    const isOpened = computed({
        set: (value: boolean) => (modalStore.openedModal = value ? MODAL_NAME : null),
        get: () => modalStore.openedModal == MODAL_NAME,
    })
</script>

<template>
    <ModalInfo>
        <div class="confirm">
            <p v-if="title" class="confirm__title h2">{{ title }}</p>
            <p v-if="text" class="confirm__text p2">{{ text }}</p>
            <div class="confirm__panel">
                <UIButton class="confirm__button">Да</UIButton>
                <UIButton class="confirm__button">Нет</UIButton>
            </div>
        </div>
    </ModalInfo>
</template>

<style lang="scss" scoped>
    .confirm {

    }
</style>