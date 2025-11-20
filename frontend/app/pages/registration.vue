<script lang="ts" setup>
    const PAGE_TITLE = 'Регистрация'
    setPageTitle(PAGE_TITLE)
    definePageMeta({
        public: true,
    })
</script>

<template>
    <LayerAuth>
        <RegistrationBase />
    </LayerAuth>
</template>

<style lang="scss" scoped>
    
</style>