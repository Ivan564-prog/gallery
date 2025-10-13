<script lang="ts" setup>
    const rootSettingsStore = useRootSettingsStore()
</script>

<template>
    <div class="wrapper">
        <NavigationSidebar class="wrapper__navigation-sidebar" />
        <div class="wrapper__content">
            <Header />
            <main class="main">
                <slot></slot>
            </main>
        </div>
    </div>
</template>

<style lang="scss" scoped>
    .wrapper {
        display: grid;
        grid-template-columns: clampFluid(313) 1fr;
        width: 100%;
        height: 100dvh;
        max-width: 1920px;
        overflow: clip;
        margin: 0 auto;
        @include tablet {
            grid-template-columns: 77px 1fr;
        }
        @include mobile {
            grid-template-columns: 1fr;
        }
    }

    .main {
        flex: 0 1 auto;
    }
</style>
