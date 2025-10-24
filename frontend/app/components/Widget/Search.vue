<script lang="ts" setup></script>

<template>
    <div class="search">
        <UIInput class="search__input" placeholder="Поиск" />
        <button class="search__button">
            <NuxtIcon class="search__button-icon" name="loupe" />
        </button>
    </div>
</template>

<style lang="scss" scoped>
    .search {
        position: relative;
        &__input {
            padding-right: clampFluid(50);
        }
        &__button {
            position: absolute;
            top: 50%;
            right: clampFluid(20);
            translate: 0 -50%;
            width: clampFluid(24);
            height: auto;
            aspect-ratio: 1;
        }
        &__button-icon {
            transition: $tr;
            @include hover {
                color: var(--color);
            }
        }
    }
</style>
