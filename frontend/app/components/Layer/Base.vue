<script lang="ts" setup>
    const rootSettingsStore = useRootSettingsStore()
</script>

<template>
    <div class="page-wrapper">
        <NavigationSidebar class="page-wrapper__navigation-sidebar" />
        <div class="page-wrapper__content">
            <Header class="page-wrapper__header" />
            <main class="main">
                <slot></slot>
            </main>
        </div>
        <ToastrError />
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
        &__content {
            position: relative;
        }
    }

    .main {
        height: calc(100dvh - clampFluid(90));
        padding: clampFluid(30) clampFluid(40) clampFluid(30) clampFluid(60);
        overflow: auto;
        @include tablet {
            padding: 20px 40px 90px;
        }
        @include mobile {
            padding: 20px 20px 90px;
        }
    }
</style>
