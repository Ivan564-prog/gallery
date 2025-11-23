<script lang="ts" setup>
    const userID = useCookie('user-id')
    const toastrStore = useToastrStore()
    const userStore = useUserStore()
    const isLoading = ref<boolean>(false)
    const params = reactive({
        name: '',
        password: '',
    })
    const errorInfo = ref<IAuthorizeErrors>({})

    const authorization = async () => {
        errorInfo.value = {}
        isLoading.value = true
        try {
            userStore.userData = await request<IUser>('/api/v1/user/authorize/', 'POST', params)
            userID.value = userStore.userData.id.toString()
            navigateTo('/')
        } catch (error) {
            toastrStore.showError('Не верный логин или пароль')
        }
        isLoading.value = false
    }
</script>

<template>
    <form class="authorize-form" @submit.prevent="authorization">
        <UILoader v-if="isLoading" class="authorize-form__loader" />
        <h2 class="authorize-form__title h1">Авторизация</h2>
        <p class="authorize-form__text p2">
            Для входа необходимо ввести логин и пароль
        </p>
        <div class="authorize-form__fields">
            <UIInput
                class="authorize-form__input"
                placeholder="Имя"
                v-model="params.name"
            />
            <UIInput
                class="authorize-form__input"
                type="password"
                placeholder="Пароль"
                v-model="params.password"
            />
        </div>
        <UILink class="authorize-form__link p2" to="/registration">Регистрация</UILink>
        <UIButton class="authorize-form__button" width-mode="full">Войти</UIButton>
    </form>
</template>

<style lang="scss" scoped>
    .authorize-form {
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
        &__loader {
            position: absolute;
            z-index: 2;
            inset: 0;
        }
        &__text {
            text-align: center;
            color: var(--gray-01);
            margin: clampFluid(16) 0 clampFluid(40);
        }
        &__fields {
            width: 100%;
            display: flex;
            flex-direction: column;
            gap: clampFluid(20);
        }
        &__link {
            align-self: flex-start;
            margin: clampFluid(30) 0 clampFluid(40);
            color: var(--gray-03);
            text-decoration: underline;
            text-decoration-skip-ink: none;
            @include hover {
                text-decoration: none;
            }
        }
    }
</style>
