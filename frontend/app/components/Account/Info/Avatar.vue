<script lang="ts" setup></script>

<template>
    <div class="avatar">
        <div class="avatar__wrapper">
            <UIImage
                class="avatar__image"
                src="/images/avatar.png"
            />
        </div>
    </div>
</template>

<style lang="scss" scoped>
    .avatar {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: clampFluid(15);
        &__wrapper {
            display: flex;
            align-items: center;
            justify-content: center;
            width: clampFluid(234);
            height: auto;
            aspect-ratio: 1;
            border-radius: 50%;
            overflow: hidden;
            background-color: var(--gray-05);
        }
        &__text {
            text-decoration: underline;
            text-decoration-skip-ink: none;
            color: var(--gray-02);
            @include hover {
                text-decoration: none;
            }
        }
        &__input {
            display: none;
        }
    }
</style>
