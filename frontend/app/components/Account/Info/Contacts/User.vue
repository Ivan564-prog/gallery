<script lang="ts" setup>
    const params = reactive({
        name: '',
        surname: '',
        patronymic: '',
        dateOfBirth: '',
        city: '',
        phone: '',
        diocese: '',
    })
</script>

<template>
    <form class="user-contacts">
        <div class="user-contacts__fields">
            <AccountInfoContactsItem title="Имя" v-model="params.name" />
            <AccountInfoContactsItem title="Фамилия" v-model="params.surname" />
            <AccountInfoContactsItem title="Отчество" v-model="params.patronymic" />
            <AccountInfoContactsItem title="Дата рождения" v-model="params.dateOfBirth" />
            <AccountInfoContactsItem title="Страна" v-model="params.city" />
            <AccountInfoContactsItem title="Федеральный округ" v-model="params.phone" />
            <AccountInfoContactsItem title="Епархия" v-model="params.diocese" />
            <AccountInfoContactsItem title="Город проживания" v-model="params.name" />
            <AccountInfoContactsItem title="Статус пользователя" v-model="params.name" />
        </div>
        <UIButton 
            class="user-contacts__button"
            size="small"
            color-variant="gray"
        >Сохранить изменения</UIButton>
    </form>
</template>

<style lang="scss" scoped>
    .user-contacts {
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