<script lang="ts" setup>
    const params = reactive({
        password: '',
        password2: '',
    })
</script>

<template>
    <form class="account-password">
        <div class="account-password__fields">
            <AccountInfoContactsItem title="Изменить пароль" v-model="params.password" />
            <AccountInfoContactsItem v-model="params.password2" />
        </div>
        <UIButton 
            class="account-password__button"
            size="small"
            color-variant="gray"
        >Сохранить новый пароль</UIButton>
    </form>
</template>

<style lang="scss" scoped>
    .account-password {
        &__fields {
            display: flex;
            flex-direction: column;
            gap: clampFluid(25);
            margin-bottom: clampFluid(30);
        }
        &__button {
            margin-left: clampFluid(260);
            @include tablet {
                width: 100%;
                margin-left: 0;
            }
        }
    }
</style>