<script lang="ts" setup>
    
</script>

<template>
    <aside class="navigation-sidebar">
        <UILink class="navigation-sidebar__logo" to="/">
            <NuxtIcon class="navigation-sidebar__logo-icon" name="logo" />
        </UILink>
        <NavigationSidebarMenu class="navigation-sidebar__menu" />
    </aside>
</template>

<style lang="scss" scoped>
    .navigation-sidebar {
        display: flex;
        flex-direction: column;
        height: 100%;
        background-color: var(--gray-06);
        &__logo {
            margin: clampFluid(20) clampFluid(41) clampFluid(35);
        }
        &__logo-icon {
            width: clampFluid(80);
            height: auto;
            aspect-ratio: 1;
            @include tablet {
                width: 50px;
            }
        }
    }
</style>