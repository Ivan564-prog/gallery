<script lang="ts" setup></script>

<template>
    <div class="loader">
        <div class="loader__icon"></div>
    </div>
</template>

<style lang="scss" scoped>
    .loader {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 100%;
        backdrop-filter: blur(4px);
        &__icon {
            border: 8px solid var(--gray-04);
            border-top: 8px solid var(--color);
            border-radius: 50%;
            width: clampFluid(80);
            height: auto;
            aspect-ratio: 1;
            animation: spin 2s linear infinite;
        }
    }
    @keyframes spin {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }
</style>
