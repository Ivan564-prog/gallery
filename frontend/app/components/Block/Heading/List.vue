<script lang="ts" setup>
    const postList = defineModel<IPostItem[]>({ required: true })
</script>

<template>
    <div class="heading-list">
        <CardPost v-for="post in postList" :key="post.id" :card-content="post" />
    </div>
</template>

<style lang="scss" scoped>
    .heading-list {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: clampFluid(20);
    }
</style>
