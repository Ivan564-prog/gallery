<script lang="ts" setup>
</script>

<template>
    <div class="authorize-layer">
        <div class="authorize-layer__head">
            <UILink class="authorize-layer__logo" to="/login">
                <NuxtIcon class="authorize-layer__logo" name="logo" />
            </UILink>
        </div>
        <div class="authorize-layer__wrapper">
            <slot></slot>
        </div>
    </div>
</template>

<style lang="scss" scoped>
    .authorize-layer {
        overflow: auto;
        height: 100dvh;
        padding-bottom: clampFluid(20);
        &__head {
            padding: clampFluid(20) clampFluid(40);
            @include tablet {
                padding: 14px 20px;
            }
        }
        &__logo {
            width: clampFluid(80);
            height: auto;
            aspect-ratio: 1;
            @include tablet {
                width: 50px;
            }
        }
    }
</style>