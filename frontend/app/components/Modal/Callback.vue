<script lang="ts" setup>
    const modalName = 'callback'
    const modalStore = useModalStore()
    const opened = computed({
        set: (value: boolean) => (modalStore.openedModal = value ? modalName : null),
        get: () => modalStore.openedModal == modalName,
    })
</script>

<template>
    <ModalBase v-model="opened">Обратная связь</ModalBase>
</template>

<style lang="scss" scoped></style>
