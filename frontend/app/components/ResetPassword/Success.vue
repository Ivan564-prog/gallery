<script lang="ts" setup>
    const MODAL_NAME = 'reset-password-success'
    const modalStore = useModalStore()
    const isOpened = computed({
        set: (value: boolean) => (modalStore.openedModal = value ? MODAL_NAME : null),
        get: () => modalStore.openedModal == MODAL_NAME,
    })

    const closeModal = () => {
        isOpened.value = false
        navigateTo('/login')
    }
</script>

<template>
    <ModalInfo v-model="isOpened">
        <div class="reset-password-modal">
            <h3 class="reset-password-modal h1">Пароль успешно обновлён</h3>
            <p class="reset-password-modal__text p1">
                Теперь вы можете войти в свой аккаунт с новым паролем.
            </p>
            <UIButton
                class="reset-password-modal__button"
                color-variant="empty-black"
                width-mode="full"
                @click="closeModal"
            >
                Войти в аккаунт
            </UIButton>
        </div>
    </ModalInfo>
</template>

<style lang="scss" scoped>
    .reset-password-modal {
        display: flex;
        flex-direction: column;
        text-align: center;
        gap: clampFluid(16);
        &__subtext {
            color: var(--gray-03);
        }
        &__button {
            margin-top: clampFluid(24);
        }
    }
</style>
