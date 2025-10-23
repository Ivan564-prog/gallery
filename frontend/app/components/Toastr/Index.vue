<script lang="ts" setup>
    const isShowed = defineModel<boolean>({ required: true })
    const toastrStore = useToastrStore()
</script>

<template>
    <Transition name="toastr">
        <div class="toastr" v-if="isShowed">
            <slot></slot>
            <UIButton 
                class="toastr__button" 
                color-variant="empty-red"
                @click="toastrStore.closeToastr"
            >
                {{ `Закрыть (${(Math.round(toastrStore.timer / 1000))})` }}
            </UIButton>
        </div>
    </Transition>
</template>

<style lang="scss" scoped>
    .toastr {
        position: fixed;
        z-index: 5;
        width: clampFluid(450);
        height: auto;
        aspect-ratio: 450 / 90;
        right: clampFluid(20);
        bottom: clampFluid(20);
        background-color: var(--gray-06);
        padding: clampFluid(15);
        display: flex;
        align-items: center;
        justify-content: center;
        gap: clampFluid(20);
        @include mobile {
            inset: 10px;
            top: auto;
            width: auto;
            aspect-ratio: 200 / 50;
        }
        &.toastr-enter-active,
        &.toastr-leave-active {
            transition: $tr;
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
        &__button {
            flex: 0 0 auto;
        }
    }
</style>
