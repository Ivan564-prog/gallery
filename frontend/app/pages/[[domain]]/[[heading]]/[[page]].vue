<script lang="ts" setup>
    const route = useRoute()
</script>

<template>
    <LayerInnerPage v-if="<string>route.params.heading" />
    <LayerIndexPage v-else />
</template>

<style lang="scss" scoped></style>
