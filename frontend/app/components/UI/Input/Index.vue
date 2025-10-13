<script lang="ts" setup>
    const { type = 'text' } = defineProps<{
        placeholder?: string
        type?: 'text' | 'tel' | 'password'
    }>()
</script>

<template>
    <UIInputText v-if="type == 'text'" :placeholder="placeholder" />
    <UIInputPhone v-else-if="type == 'tel'" :placeholder="placeholder" />
    <UIInputPassword v-else-if="type == 'password'" :placeholder="placeholder" />
</template>

<style lang="scss" scoped></style>
