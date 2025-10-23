<script lang="ts" setup>
    const userStore = useUserStore()
    const toastrStore = useToastrStore()
    const params = reactive({
        name: userStore.userData?.name,
        surname: userStore.userData?.surname,
        patronymic: userStore.userData?.patronymic,
        city: userStore.userData?.city,
        phone: userStore.userData?.phone || '',
        diocese: userStore.userData?.diocese,
        country: userStore.userData?.country,
        region: userStore.userData?.region,
    })
    const errorInfo = ref<IUserErrors>({})

    const setUserData = async () => {
        errorInfo.value = {}
        try {
            userStore.userData = await request<IUser>('/api/v1/user/', 'PATCH', params)
            toastrStore.showSuccess('Данные пользователя успешно обновлены')
        } catch (error) {
            errorInfo.value = (error as IErrorRequest<IUserErrors>).data
            window.scrollTo({
                top: 0,
                behavior: 'smooth',
            })
        }
    }

</script>

<template>
    <form class="user-contacts" @submit.prevent="setUserData">
        <div class="user-contacts__fields">
            <AccountInfoContactsItem 
                placeholder="Введите" 
                title="Имя" 
                v-model="params.name" 
            />
            <AccountInfoContactsItem 
                placeholder="Введите" 
                title="Фамилия" 
                v-model="params.surname" 
            />
            <AccountInfoContactsItem 
                placeholder="Введите" 
                title="Отчество" 
                v-model="params.patronymic" 
            />
            <AccountInfoContactsItem 
                readonly
                title="Дата рождения"
                :model-value="userStore.userData?.dateOfBirth" 
            />
            <AccountInfoContactsItem 
                placeholder="Введите" 
                title="Страна" 
                v-model="params.country" 
            />
            <AccountInfoContactsItem 
                placeholder="Введите" 
                title="Федеральный округ"
                v-model="params.region" 
            />
            <AccountInfoContactsItem 
                readonly
                placeholder="Введите" 
                title="Епархия" 
                :model-value="userStore.userData?.diocese?.title" 
            />
            <AccountInfoContactsItem 
                placeholder="Введите" 
                title="Город проживания"
                v-model="params.city" 
            />
            <AccountInfoContactsItem 
                placeholder="Введите" 
                title="Телефон" 
                type="tel"
                :error-text="errorInfo.phone && errorInfo.phone[0]"
                v-model="params.phone" 
            />
            <AccountInfoContactsItem 
                readonly
                title="Почта" 
                :model-value="userStore.userData?.email" 
            />
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