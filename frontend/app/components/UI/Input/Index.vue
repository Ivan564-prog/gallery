<script lang="ts" setup>
    const { type = 'text' } = defineProps<{
        type?: 'text' | 'tel' | 'password'
    }>()
</script>

<template>
    <UIInputText v-if="type == 'text'" />
    <UIInputPhone v-else-if="type == 'tel'" />
    <UIInputPassword v-else-if="type == 'password'" />
</template>

<style lang="scss" scoped></style>
