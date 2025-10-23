<script lang="ts" setup>
    const MODAL_NAME = 'confirm'
    const modalStore = useModalStore()
    const confirmStore = useConfirmStore()
    const isOpened = computed({
        set: (value: boolean) => (modalStore.openedModal = value ? MODAL_NAME : null),
        get: () => modalStore.openedModal == MODAL_NAME,
    })
</script>

<template>
    <ModalInfo v-model="isOpened">
        <div class="confirm">
            <p v-if="confirmStore.titleWindow" class="confirm__title h2">{{ confirmStore.titleWindow }}</p>
            <p v-if="confirmStore.textWindow" class="confirm__text p2">{{ confirmStore.textWindow }}</p>
            <div class="confirm__panel">
                <UIButton 
                    class="confirm__button" 
                    width-mode="full"
                    @click="confirmStore.confirm"
                >Да</UIButton>
                <UIButton 
                    class="confirm__button" 
                    width-mode="full"
                    color-variant="gray"
                    @click="confirmStore.cancel"
                >Нет</UIButton>
            </div>
        </div>
    </ModalInfo>
</template>

<style lang="scss" scoped>
    .confirm {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: clampFluid(20);
        width: 100%;
        &__panel {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: clampFluid(12);
            width: 100%;
        }
    }
</style>