<script lang="ts" setup></script>

<template>
    <div class="authorize-layer">
        <UILink class="authorize-layer__logo" to="/login">
            <NuxtIcon filled class="authorize-layer__logo-icon" name="logo" />
        </UILink>
        <div class="authorize-layer__wrapper">
            <slot></slot>
        </div>
        <ToastrError />
        <ToastrSuccess />
    </div>
</template>

<style lang="scss" scoped>
    .authorize-layer {
        position: relative;
        height: 100dvh;
        overflow: auto;
        &__head {
            position: absolute;
            top: 0;
            left: 0;
            padding: clampFluid(20) clampFluid(40);
            @include tablet {
                padding: 14px 20px;
            }
        }
        &__logo {
            position: absolute;
            z-index: 2;
            top: clampFluid(20);
            left: clampFluid(40);
            width: clampFluid(80);
            height: auto;
            aspect-ratio: 1;
            @include tablet {
                width: 50px;
            }
        }
        &__wrapper {
            padding-bottom: clampFluid(20);
        }
    }
</style>
