<script lang="ts" setup>
    const { breadcrumbs } = defineProps<{ breadcrumbs: IBreadcrumb[] }>()
</script>

<template>
    <div itemscope itemtype="http://schema.org/BreadcrumbList">
        <span itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
            <a itemprop="item" href="/">
                <span itemprop="name">Главная</span>
            </a>
            <meta itemprop="position" content="1" />
        </span>
        <span
            itemprop="itemListElement"
            itemscope
            itemtype="https://schema.org/ListItem"
            v-for="(breadcrumb, i) in breadcrumbs"
        >
            <a itemprop="item" :href="breadcrumb.link">
                <span itemprop="name">{{ breadcrumb.title }}</span>
            </a>
            <meta itemprop="position" :content="(i + 2).toString()" />
        </span>
    </div>
</template>

<style lang="scss" scoped>
    div {
        display: none;
    }
</style>
