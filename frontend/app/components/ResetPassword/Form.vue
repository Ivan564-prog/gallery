<script lang="ts" setup>
    const modalStore = useModalStore()
    const isLoading = ref<boolean>(false)
    const params = reactive({
        email: '',
    })
    const errorInfo = ref<IResetPasswordErrors>({})

    const authorization = async () => {
        errorInfo.value = {}
        isLoading.value = true
        try {
            await request(
                '/api/v1/user/send_reset_password/', 
                'POST', 
                params
            )
            modalStore.openedModal = 'reset-password-success'
        } catch (error) {
            errorInfo.value = (error as IHttpError<IResetPasswordErrors>).data
        }
        isLoading.value = false
    }
</script>

<template>
    <form class="authorize-form" @submit.prevent="authorization">
        <UILoader v-if="isLoading" class="authorize-form__loader" />
        <h2 class="authorize-form__title h1">Забыли пароль?</h2>
        <p class="authorize-form__text p2">Введите адрес электронной почты, с которым <br> вы регистрировались.</p>
        <div class="authorize-form__fields">
            <UIInput 
                class="authorize-form__input" 
                placeholder="Почта"
                :error-text="errorInfo.email && errorInfo.email[0]"
                v-model="params.email"
            />
        </div>
        <UIButton 
            class="authorize-form__button"
            width-mode="full"
        >Отправить письмо</UIButton>
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
            margin-bottom: clampFluid(20);
        }
    }
</style>