<script lang="ts" setup>
    const modelValue = defineModel<string>()
    const searchQuery = ref<string>('')

    const search = () => {
        modelValue.value = searchQuery.value
    }
</script>
    
<template>
    <form class="search" @submit.prevent="search">
        <UIInput class="search__input" placeholder="Поиск" v-model="searchQuery" />
        <button class="search__button">
            <NuxtIcon class="search__button-icon" name="loupe" />
        </button>
    </form>
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
