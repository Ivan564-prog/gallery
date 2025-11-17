<script lang="ts" setup>
    const PAGE_TITLE = 'Авторизация'
    setPageTitle(PAGE_TITLE)
    definePageMeta({
        public: true,
    })
</script>

<template>
    <LayerAuth>
        <AuthorizeBase />
    </LayerAuth>
</template>

<style lang="scss" scoped></style>
