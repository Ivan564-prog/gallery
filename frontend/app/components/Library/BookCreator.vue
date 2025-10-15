<script lang="ts" setup>
    const MODAL_NAME = 'book-creator'
    const modalStore = useModalStore()
    const opened = computed({
        set: (value: boolean) => (modalStore.openedModal = value ? MODAL_NAME : null),
        get: () => modalStore.openedModal == MODAL_NAME,
    })
</script>

<template>
    <ModalBase v-model="opened">
        <template v-slot:head>
            <h2 class="book-creator-title h2">Новая публикация</h2>
        </template>
        <template v-slot:main>
            <form id="creatorBook" class="book-creator-form">
                <div class="book-creator-form__top"></div>
                <div class="book-creator-form__bottom"></div>
            </form>
        </template>
        <template v-slot:footer>
            <div class="book-creator-footer">
                <UIButton 
                    class="book-creator-footer__button"
                    font-size="big"
                >Добавить публикацию</UIButton>
                <UIButton 
                    class="book-creator-footer__button" 
                    color-variant="gray"
                    font-size="big"
                >Сохранить черновик</UIButton>
                <button class="book-creator-footer__remove-button p1 p1--bold">Удалить</button>
            </div>
        </template>
    </ModalBase>
</template>

<style lang="scss" scoped>
    .book-creator-footer {
        display: flex;
        align-items: center;
        gap: clampFluid(10);
        &__remove-button {
            padding: 0 clampFluid(30);
            height: clampFluid(59);
            transition: $tr;
            @include hover {
                color: var(--color);
            }
        }
    }
</style>