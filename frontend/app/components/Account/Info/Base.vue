<script lang="ts" setup>
    const userStore = useUserStore()
</script>

<template>
    <div class="account-info">
        <AccountInfoAvatar 
            class="account-info__avatar" 
            :avatar="userStore.userData?.image"
        />
        <div class="account-info__wrapper">
            <AccountInfoContactsBase class="account-info__contacts" />
            <AccountInfoPassword class="account-info__password" />
        </div>
    </div>
</template>

<style lang="scss" scoped>
    .account-info {
        display: grid;
        grid-template-columns: clampFluid(234) 1fr;
        gap: clampFluid(82);
        @include tablet {
            grid-template-columns: 1fr;
            gap: 20px;
        }
        &__password {
            margin-top: clampFluid(50);
            @include tablet {
                margin-top: 40px;
            }
        }
    }
</style>