<script lang="ts" setup>
    defineProps<{
        cardContent: IPostItem
    }>()
</script>

<template>
    <UILink class="post-card" :to="cardContent.link">
        <UIImage class="post-card__image" :src="cardContent.image" :alt="cardContent.title" />
        <p class="post-card__title p1">{{ cardContent.title }}</p>
        <p1 class="post-card__description p2">{{ cardContent.description }}</p1>
    </UILink>
</template>

<style lang="scss" scoped></style>
