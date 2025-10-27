<script lang="ts" setup>
    const userStore = useUserStore()
</script>

<template>
    <div class="account-contacts">
        <AccountInfoContactsDiocese v-if="userStore.userData?.role === 'admin'" />
        <AccountInfoContactsUser v-else />
    </div>
</template>

<style lang="scss" scoped></style>
