<script lang="ts" setup>
    const { data: indexSettings } = await useRequest<IIndexSettings>('/api/v1/config/index/')
    const config = useRuntimeConfig()

    setSeoMeta(indexSettings.value)
</script>

<template>
    <div class="index-page">
        <UIButton class="index-page__button" to="#callback">Click</UIButton>
    </div>
</template>

<style lang="scss" scoped>
    .index-page {
        &__slider-input {
        }
    }

    .slider-input {
        display: grid;
        grid-template-columns: 60px 300px;
        gap: 20px;
        align-items: center;
        padding: 20px;
    }

    .slider-input-range {
        display: grid;
        grid-template-columns: 60px 60px 300px;
        gap: 20px;
        align-items: center;
        padding: 20px;
    }
</style>
