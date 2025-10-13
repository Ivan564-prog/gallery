<script lang="ts" setup>
    const { error } = defineProps<{
        error: any
    }>()
</script>

<template>
    <LayerBase>
        <div class="not-found">
            {{ error.statusCode }}
            <br />
            {{ error.message }}
            {{ error.cause }}
            {{ error }}
        </div>
    </LayerBase>
</template>

<style lang="scss" scoped>
    .page-content {
        width: 100%;
        min-height: 100vh;
        overflow: clip;
        display: flex;
        flex-direction: column;
    }

    .not-found {
        display: flex;
        height: 100%;
        width: 100%;
        align-items: center;
        justify-content: center;
        margin: auto 0 0;
    }
</style>
