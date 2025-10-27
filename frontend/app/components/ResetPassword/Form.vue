<script lang="ts" setup>
    const route = useRoute()
    const toastrStore = useToastrStore()
    const modalStore = useModalStore()
    const isLoading = ref<boolean>(false)
    const params = reactive({
        password: '',
        password2: '',
    })
    const errorInfo = ref<IPasswordErrors>({})

    const authorization = async () => {
        errorInfo.value = {}
        isLoading.value = true
        try {
            await request('/api/v1/user/reset_password/', 'POST', {
                ...route.query,
                ...params,
            })
            modalStore.openedModal = 'reset-password-success'
        } catch (error) {
            const errorMessage = (error as IHttpError<IPasswordErrors>).data.nonFieldErrors
            if (errorMessage?.length) toastrStore.showError(errorMessage[0]!)
        }
        isLoading.value = false
    }
</script>

<template>
    <form class="authorize-form" @submit.prevent="authorization">
        <UILoader v-if="isLoading" class="authorize-form__loader" />
        <h2 class="authorize-form__title h1">Придумайте новый пароль</h2>
        <p class="authorize-form__text p2">Введите новый пароль и повторите его для подтверждения.</p>
        <div class="authorize-form__fields">
            <UIInput
                class="authorize-form__input"
                type="password"
                placeholder="Пароль"
                v-model="params.password"
            />
            <UIInput
                class="authorize-form__input"
                type="password"
                placeholder="Повторите пароль"
                v-model="params.password2"
            />
        </div>
        <UIButton class="authorize-form__button" width-mode="full">Сохранить пароль</UIButton>
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
            display: flex;
            flex-direction: column;
            gap: clampFluid(20);
            width: 100%;
            margin-bottom: clampFluid(20);
        }
    }
</style>
