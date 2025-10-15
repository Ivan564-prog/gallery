<script lang="ts" setup>
    
</script>

<template>
    <aside class="navigation-sidebar">
        <UILink class="navigation-sidebar__logo mobile-hidden" to="/">
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
        @include mobile {
            position: fixed;
            z-index: 5;
            bottom: 0;
            left: 0;
            width: 100%;
            height: auto;
            padding-inline: 10px;
        }
        &__logo {
            margin: clampFluid(20) clampFluid(41) clampFluid(35);
            @include tablet {
                margin: 12px 14px 19px;
            }
        }
        &__logo-icon {
            width: clampFluid(80);
            height: auto;
            aspect-ratio: 1;
            color: var(--black);
            @include tablet {
                width: 50px;
            }
        }
    }
</style>