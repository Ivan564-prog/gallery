<script lang="ts" setup>
    const settingsStore = useRootSettingsStore()
</script>

<template>
    <header class="header">
        <div class="header__content">
            <UILink class="header__logo desktop-hidden" to="/">
                <NuxtIcon class="header__logo-icon" name="logo" />
            </UILink>
            <h1 class="header__title h1">{{ settingsStore.pageTitle }}</h1>
        </div>
        <HeaderAccountLinks class="header__account-links" />
    </header>
</template>

<style lang="scss" scoped>
   .header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
        height: clampFluid(90);
        padding: 0 clampFluid(40) 0 clampFluid(60);
        box-shadow: 0 0 30px 0 rgba(0, 0, 0, 0.05);
        background-color: var(--white);
        @include tablet {
            padding: 15px 40px;
        }
        @include mobile {
            padding: 15px 20px;
        }
        &__logo-icon {
            width: 50px;
            height: 50px;
            color: var(--black);
        }
   }
</style>
