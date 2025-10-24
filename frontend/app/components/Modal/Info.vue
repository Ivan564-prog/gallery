<script lang="ts" setup>
    const isOpened = defineModel()
    const modalStore = useModalStore()

    const closeModal = () => (isOpened.value = false)

    const clickKeyboardHandler = (event: KeyboardEvent) => {
        if (event.key === 'Escape') closeModal()
    }

    watch(isOpened, newValue => {
        if (!newValue) modalStore.optionalData = {}
    })

    onMounted(() => {
        document.addEventListener('keydown', clickKeyboardHandler)
    })
    onUnmounted(() => {
        document.removeEventListener('keydown', clickKeyboardHandler)
    })
</script>

<template>
    <Transition name="modal">
        <div v-if="isOpened" class="info-modal">
            <button class="info-modal__close-bg" @click="closeModal"></button>
            <div class="info-modal__wrapper">
                <div class="info-modal__container">
                    <slot></slot>
                </div>
            </div>
        </div>
    </Transition>
</template>

<style lang="scss" scoped>
    .info-modal {
        $this: &;
        position: fixed;
        inset: 0;
        z-index: 10;
        width: 100vw;
        height: 100dvh;
        &.modal-enter-active,
        &.modal-leave-active {
            transition: $tr;
            #{$this}__container {
                transition: $tr;
            }
        }
        &.modal-enter-from,
        &.modal-leave-to {
            opacity: 0;
            #{$this}__container {
                translate: 0 -100%;
            }
        }
        &.modal-enter-to,
        &.modal-leave-from {
            opacity: 1;
            #{$this}__container {
                translate: 0 0;
            }
        }
        &__wrapper {
            position: absolute;
            top: 0;
            left: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100vw;
            height: 100dvh;
            overflow-x: hidden;
            overflow-y: auto;
        }
        &__container {
            position: relative;
            z-index: 6;
            width: clampFluid(800);
            height: fit-content;
            padding: clampFluid(60);
            background-color: var(--gray-06);
            @include tablet {
                width: 80%;
            }
        }
        &__close-bg {
            position: absolute;
            z-index: 5;
            inset: 0;
            background-color: rgba(#000, 0.5);
        }
        &__main {
            flex: 1 0 auto;
        }
    }
</style>
