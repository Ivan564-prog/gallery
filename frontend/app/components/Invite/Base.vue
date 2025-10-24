<script lang="ts" setup>
    const userStore = useUserStore()
</script>

<template>
    <div class="invite">
        <InviteMissioner v-if="userStore.userData?.role === 'chief'" />
        <InviteChiefMissionary v-else-if="userStore.userData?.role === 'admin'" />
        <InviteDiocese v-else />
    </div>
</template>

<style lang="scss" scoped></style>
