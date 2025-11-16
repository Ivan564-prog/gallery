<script lang="ts" setup>
    const toastrStore = useToastrStore()
    const isCheckPolitic = ref<boolean>(false)
    const errorInfo = ref<IUserErrors & IPasswordErrors>({})
    const params = reactive({
        name: '',
        role: '',
        password: '',
        password2: '',
    })

    const registrationUser = async () => {
        if (!isCheckPolitic.value) {
            toastrStore.showError('Подтвердите согласие с правилами обработки персональной информации')
            return
        }
        if (params.password !== params.password2) {
            toastrStore.showError('Пароли не совпадают')
            return
        }
        errorInfo.value = {}

        try {
            await request('/api/v1/user/', 'POST', params)
            navigateTo('/login')
        } catch (error) {
            const errorMessage = (error as IHttpError<string>).data
            toastrStore.showError(errorMessage)
        }
    }
</script>

<template>
    <form class="user-form" @submit.prevent="registrationUser">
        <div class="user-form__info">
            <h1 class="user-form__title h1">Регистрация</h1>
            <p class="user-form__text p2">Для создания учётной записи заполните информацию о себе.</p>
        </div>
        <div class="user-form__fields">
            <div class="user-form__item info-item">
                <p class="info-item__title p3">Имя</p>
                <UIInput 
                    class="info-item__field" 
                    placeholder="Имя" 
                    v-model="params.name" 
                />
            </div>
            <div class="user-form__item info-item">
                <p class="info-item__title p3">Роль</p>
                <UISelect
                    placeholder="Выберет роль" 
                    :items="{
                        'admin': 'Админ',
                        'user': 'Пользователь',
                    }" 
                    v-model="params.role"
                />
            </div>
            <div class="user-form__item info-item">
                <p class="info-item__title p3">Придумайте пароль</p>
                <UIInput 
                    class="info-item__field" 
                    placeholder="Пароль" 
                    type="password"
                    v-model="params.password" 
                />
                <UIInput 
                    class="info-item__field" 
                    placeholder="Повторите пароль" 
                    type="password"
                    v-model="params.password2" 
                />
            </div>
        </div>
        <WidgetPoliticConfirm v-model="isCheckPolitic" />
        <UIButton 
            class="user-form__button"
            width-mode="full"
        >Зарегистрироваться</UIButton>
    </form>
</template>

<style lang="scss" scoped>
    .user-form {
        display: flex;
        flex-direction: column;
        gap: clampFluid(30);
        @include tablet {
            gap: 20px;
        }
        &__info {
            display: flex;
            flex-direction: column;
            gap: clampFluid(10);
            text-align: center;
        }
        &__fields {
            display: flex;
            flex-direction: column;
            gap: clampFluid(20);
        }
    }

    .info-item {
        display: flex;
        flex-direction: column;
        gap: clampFluid(8);
        &__title {
            color: var(--gray-03);
        }
    }
</style>