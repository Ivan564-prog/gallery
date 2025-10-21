<script lang="ts" setup>
    const opened = defineModel()
    const slots = useSlots()
    const modalStore = useModalStore()

    const closeModal = () => (opened.value = false)

    const clickKeyboardHandler = (event: KeyboardEvent) => {
        if (event.key === 'Escape') closeModal()
    }

    watch(opened, newValue => {
        if (!newValue)
            modalStore.optionalData = {}
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
        <div v-if="opened" class="base-modal">
            <button class="base-modal__close-bg" @click="closeModal"></button>
            <div class="base-modal__wrapper">
                <div class="base-modal__container">
                    <div class="base-modal__head modal-head">
                        <div class="modal-head__content">
                            <slot name="head"></slot>
                        </div>
                        <button class="base-modal__close" @click="closeModal">
                            <NuxtIcon class="base-modal__close-icon" name="close" />
                            <span class="base-modal__close-text p2 p2--bold mobile-hidden">Закрыть</span>
                        </button>
                    </div>
                    <div v-if="slots.main" class="base-modal__main modal-main" :opened="opened">
                        <div class="modal-main__content">
                            <slot name="main"></slot>
                        </div>
                    </div>
                    <div class="base-modal__footer modal-footer">
                        <slot name="footer"></slot>
                    </div>
                </div>
            </div>
        </div>
    </Transition>
</template>

<style lang="scss" scoped>
    .base-modal {
        $this: &;
        position: fixed;
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
                translate: 100% 0;
                @include tablet {
                    translate: 0 100%;
                }
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
            justify-content: flex-end;
            width: 100vw;
            height: 100dvh;
            overflow-x: hidden;
            overflow-y: auto;
        }
        &__container {
            position: relative;
            z-index: 6;
            display: flex;
            flex-direction: column;
            gap: clampFluid(30);
            width: 70%;
            min-height: 100%;
            height: fit-content;
            background-color: var(--gray-06);
            @include tablet {
                width: 100%;
            }
        }
        &__close {
            flex: 0 0 auto;
            display: flex;
            align-items: center;
            gap: clampFluid(20);
            padding: clampFluid(16) clampFluid(20);
            color: var(--white);
            background-color: var(--gray-02);
            transition: $tr;
            @include hover {
                background-color: var(--gray-01);
            }
            @include tablet-gt {
                position: absolute;
                left: 0;
                top: clampFluid(30);
                translate: -100% 0;
            }
            @include tablet {
                width: 40px;
                height: 40px;
            }
        }
        &__close-icon {
            width: clampFluid(20);
            height: auto;
            aspect-ratio: 1;
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

    .modal-head {
        position: sticky;
        z-index: 5;
        top: 0;
        display: flex;
        justify-content: space-between;
        padding: clampFluid(20) clampFluid(40) clampFluid(10);
        background-color: var(--gray-06);
        @include tablet {
            align-items: center;
            padding: 20px 20px 5px;
        }
        &__content {
            flex: 1 1 auto;
        }
    }

    .modal-main {
        padding: 0 clampFluid(40);
        @include tablet {
            padding: 0 20px;
        }
        &__content {
            height: 100%;
            padding: clampFluid(40);
            background-color: var(--white);
            @include tablet {
                padding: 20px;
            }
        }
    }

    .modal-footer {
        position: sticky;
        z-index: 1;
        bottom: 0;
        padding: clampFluid(30) clampFluid(40);
        background-color: var(--white);
        border-top: 2px solid var(--gray-06);
    }
</style>
