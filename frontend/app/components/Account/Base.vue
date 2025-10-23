<script lang="ts" setup>
    const currentTab = ref<number>(1)
</script>

<template>
    <section class="account">
        <AccountHead class="account__head" v-model="currentTab" />
        <div class="account__wrapper">
            <AccountInfoBase v-if="currentTab === 1" />
            <InviteBase v-else />
        </div>
    </section>
</template>

<style lang="scss" scoped>
    .account {
        &__wrapper {
            display: flex;
            flex-direction: column;
            justify-content: center;
            height: 100%;
            margin-top: clampFluid(32);
        }
    }
</style>