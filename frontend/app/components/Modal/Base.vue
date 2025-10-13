<script lang="ts" setup>
    const opened = defineModel()

    const closeModal = () => (opened.value = false)

    const clickKeyboardHandler = (event: KeyboardEvent) => {
        if (event.key === 'Escape') closeModal()
    }

    onMounted(() => {
        document.addEventListener('keydown', clickKeyboardHandler)
    })
    onUnmounted(() => {
        document.removeEventListener('keydown', clickKeyboardHandler)
    })
</script>

<template>
    <Transition name="modal">
        <div class="base-modal" v-if="opened">
            <div class="base-modal__close-bg" @click="closeModal"></div>
            <div class="base-modal__container">
                <div class="base-modal__close" @click="closeModal">✕</div>
                <slot></slot>
            </div>
        </div>
    </Transition>
</template>

<style lang="scss" scoped>
    .base-modal {
        $this: &;
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-color: rgba($color: #000, $alpha: 0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10;
        &.modal-enter-active,
        &.modal-leave-active {
            transition: 0.3s;
            #{$this}__container {
                transition: 0.3s;
            }
        }
        &.modal-enter-from,
        &.modal-leave-to {
            opacity: 0;
            #{$this}__container {
                translate: 0 100%;
            }
        }
        &.modal-enter-to,
        &.modal-leave-from {
            opacity: 1;
            #{$this}__container {
                translate: 0 0;
            }
        }
        &__container {
            width: fit-content;
            max-height: 60vh;
            height: fit-content;
            min-height: 100px;
            min-width: 200px;
            background-color: #fff;
            position: relative;
            overflow: auto;
            display: flex;
            flex-direction: column;
        }
        &__close {
            width: 30px;
            height: 30px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            position: absolute;
            top: 10px;
            right: 10px;

            &:hover {
                color: #f00;
            }
        }
        &__close-bg {
            position: absolute;
            width: 100%;
            height: 100%;
            left: 0;
            top: 0;
        }
    }
</style>
