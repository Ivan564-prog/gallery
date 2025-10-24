<script lang="ts" setup>
    const isLoading = ref<boolean>(false)
    const params = reactive({
        email: '',
        password: '',
    })
    const errorInfo = ref<IAuthorizeErrors>({})

    const authorization = async () => {
        errorInfo.value = {}
        isLoading.value = true
        try {
            await request('/api/v1/user/authorize/', 'POST', params)
            navigateTo('/')
        } catch (error) {
            errorInfo.value = (error as IHttpError<IAuthorizeErrors>).data
        }
        isLoading.value = false
    }
</script>

<template>
    <form class="authorize-form" @submit.prevent="authorization">
        <UILoader v-if="isLoading" class="authorize-form__loader" />
        <h2 class="authorize-form__title h1">Авторизация</h2>
        <p class="authorize-form__text p2">
            Для входа необходимо ввести адрес
            <br />
            электронной почты и пароль
        </p>
        <div class="authorize-form__fields">
            <UIInput
                class="authorize-form__input"
                placeholder="Почта"
                :error-text="errorInfo.email && errorInfo.email[0]"
                v-model="params.email"
            />
            <UIInput
                class="authorize-form__input"
                type="password"
                placeholder="Пароль"
                :error-text="errorInfo.password && errorInfo.password[0]"
                v-model="params.password"
            />
        </div>
        <UILink class="authorize-form__link p2" to="/forgot-password">Забыли пароль?</UILink>
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
