<script lang="ts" setup>
    const { filled = false } = defineProps<{
        name: string
        filled?: boolean
    }>()
</script>

<template>
    <svg v-if="!filled" class="icon" aria-hidden="true">
        <use :xlink:href="`#${name}`" />
    </svg>
    <NuxtIcon v-else class="icon" filled :name="name" />
</template>

<style lang="scss" scoped>
    .icon {
        height: auto;
    }
</style>
