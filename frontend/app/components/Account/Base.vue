<script lang="ts" setup>
    const currentTab = ref<number>(1)
</script>

<template>
    <section class="account">
        <AccountHead class="account__head" v-model="currentTab" />
        <div class="account__wrapper">
            <AccountInfoBase />
        </div>
    </section>
</template>

<style lang="scss" scoped>
    .account {
        &__wrapper {
            margin-top: clampFluid(32);
        }
    }
</style>