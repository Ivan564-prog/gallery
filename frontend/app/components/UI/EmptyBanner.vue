<script lang="ts" setup>
    const { title = 'Ничего нет' } = defineProps<{
        title?: string
    }>()
</script>

<template>
    <div class="empty-banner">
        <p class="empty-banner__title h2">{{ title }}</p>
    </div>
</template>

<style lang="scss" scoped>
    .empty-banner {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 100%;
    }
</style>
