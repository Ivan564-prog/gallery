<script lang="ts" setup>
    const isShowed = defineModel<boolean>({ required: true })
    const toastrStore = useToastrStore()
</script>

<template>
    <Transition name="toastr">
        <div class="toastr" v-if="isShowed">
            <NuxtIcon class="toastr__close" name="close" @click="toastrStore.closeToastr" />
            <slot></slot>
            <div class="toastr__progressbar" :style="{ width: `${(toastrStore.timer / 4000) * 100}%` }"></div>
        </div>
    </Transition>
</template>

<style lang="scss" scoped>
    .toastr {
        position: fixed;
        z-index: 5;
        width: clampFluid(250);
        height: auto;
        aspect-ratio: 200 / 90;
        right: clampFluid(20);
        bottom: clampFluid(20);
        background-color: var(--white);
        padding: clampFluid(20);
        display: flex;
        align-items: center;
        justify-content: center;
        @include mobile {
            inset: 10px;
            top: auto;
            width: auto;
            aspect-ratio: 200 / 50;
        }
        &.toastr-enter-active,
        &.toastr-leave-active {
            @include transition;
        }
        &.toastr-enter-from,
        &.toastr-leave-to {
            opacity: 0;
            translate: 0 100%;
        }
        &.toastr-enter-to,
        &.toastr-leave-from {
            opacity: 1;
            translate: 0 0;
        }
        &__close {
            position: absolute;
            top: clampFluid(10);
            right: clampFluid(10);
            width: clampFluid(20);
            height: auto;
            aspect-ratio: 1;
            cursor: pointer;
        }
        &__progressbar {
            position: absolute;
            bottom: 0;
            left: 0;
            height: 2px;
            background-color: var(--color-main);
        }
    }
</style>
