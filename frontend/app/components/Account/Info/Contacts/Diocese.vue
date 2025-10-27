<script lang="ts" setup>
    const userStore = useUserStore()
</script>

<template>
    <div class="diocese-contacts">
        <AccountInfoContactsItem 
            placeholder="Введите" 
            title="Название" 
            :model-value="userStore.userData?.name" 
        />
        <AccountInfoContactsItem 
            placeholder="Почта" 
            title="Фамилия" 
            :model-value="userStore.userData?.email" 
        />
    </div>
</template>

<style lang="scss" scoped>
    .diocese-contacts {
        display: flex;
        flex-direction: column;
        gap: clampFluid(25);
    }
</style>