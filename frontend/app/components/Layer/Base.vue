<script lang="ts" setup>
    const rootSettingsStore = useRootSettingsStore()
</script>

<template>
    <div class="page-wrapper">
        <NavigationSidebar class="page-wrapper__navigation-sidebar" />
        <div class="page-wrapper__content">
            <Header />
            <main class="main">
                <slot></slot>
            </main>
        </div>
    </div>
</template>

<style lang="scss" scoped>
    .page-wrapper {
        display: grid;
        grid-template-columns: clampFluid(313) 1fr;
        width: 100%;
        height: 100%;
        @include tablet {
            grid-template-columns: 77px 1fr;
        }
        @include mobile {
            grid-template-columns: 1fr;
        }
    }

    .main {
        padding: clampFluid(30) clampFluid(40) clampFluid(30) clampFluid(60);
        flex: 0 1 auto;
    }
</style>
