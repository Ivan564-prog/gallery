<script lang="ts" setup>
    const route = useRoute()
    const toastrStore = useToastrStore()
    const isCheckPolitic = ref<boolean>(false)
    const params = reactive({
        password1: '',
        password2: '',
        code: route.query.code,
    })
    const errorInfo = ref<IPasswordErrors & IUserErrors>({})

    const registration = async () => {
        if (!isCheckPolitic.value) {
            toastrStore.showError('Подтвердите согласие с правилами обработки персональной информации')
            return
        }
        errorInfo.value = {}

        try {
            await request('/api/v1/user/register/', 'POST', params)
            navigateTo('/login')
        } catch (error) {
            const errorMessage = (error as IHttpError<IPasswordErrors>).data.nonFieldErrors
            if (errorMessage?.length) toastrStore.showError(errorMessage[0]!)
            errorInfo.value = (error as IHttpError<IUserErrors>).data
        }
    }
</script>

<template>
    <form class="diocese-form" @submit.prevent="registration">
        <div class="diocese-form__info">
            <h1 class="diocese-form__title h1">Регистрация</h1>
            <p class="diocese-form__text p2">Для создания учётной записи епархии заполните информацию о себе.</p>
        </div>
        <div class="diocese-form__fields">
            <UIInput
                class="diocese-form__input"
                type="password"
                placeholder="Пароль"
                :error-text="errorInfo.password1 && errorInfo.password1[0]"
                v-model="params.password1"
            />
            <UIInput
                class="diocese-form__input"
                type="password"
                placeholder="Повторите пароль"
                v-model="params.password2"
            />
        </div>
        <WidgetPoliticConfirm v-model="isCheckPolitic" />
        <UIButton 
            class="diocese-form__button"
            width-mode="full"
        >Зарегистрироваться</UIButton>
    </form>    
</template>

<style lang="scss" scoped>
    .diocese-form {
        display: flex;
        flex-direction: column;
        gap: clampFluid(30);
        &__info {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            gap: clampFluid(10);
        }
        &__text {
            color: var(--gray-01);
        }
        &__fields {
            display: flex;
            flex-direction: column;
            gap: clampFluid(8);
        }
    }
</style>