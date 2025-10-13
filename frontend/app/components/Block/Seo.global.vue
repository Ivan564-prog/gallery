<script lang="ts" setup>
    const modelValue = defineModel<ISeoBlock>({ required: true })
</script>

<template>
    <div class="seo">
        <div class="seo__container container">
            <div class="seo__text content-text" v-html="modelValue.text"></div>
            <NuxtImg v-if="modelValue.image" class="seo__image" :src="modelValue.image" />
        </div>
    </div>
</template>

<style lang="scss" scoped>
    .seo {
        &__container {
            display: grid;
            grid-template-columns: 1fr 1.2fr;
            gap: 40px;
        }
        &__text {
            width: 100%;
        }
        &__image {
            width: 100%;
            height: auto;
            aspect-ratio: 16 / 9;
        }
    }
</style>
