<script lang="ts" setup>
    const isActualLink = ref<boolean>()
    const passwordData = reactive({
        password1: '',
        password2: '',
    })
    const toastrStore = useToastrStore()

    const resetData = () => {
        passwordData.password1 = ''
        passwordData.password2 = ''
    }

    const resetPassword = async () => {
        try {
            await useRequest<TRequestBody>('/api/v1/user/reset_password/', 'POST', {
                ...passwordData,
            })
            toastrStore.showSuccess('Пароль изменен')
            resetData()
        } catch (error: any) {
            if ((error as IHttpError<TRequestBody>).data.nonFieldErrors)
                toastrStore.showError((error as IHttpError<TRequestBody>).data.nonFieldErrors[0])
        }
    }
    const checkResetLink = async () => {
        try {
            await useRequest('/api/v1/user/check_reset/', 'GET', useRoute().query)
        } catch (error: any) {
            if (error.status == 400) {
                isActualLink.value = false
            } else if (error.status == 404) {
                throw error
            }
        }
        isActualLink.value = true
    }
    checkResetLink()
    setSeoMeta({
        title: 'Смена пароля',
    })
</script>

<template>
    <div class="password-reset container">
        <p v-if="isActualLink === false" class="h2">Срок действия ссылки истек</p>
        <p class="password-reset__title h2">Сменить пароль</p>
        <form class="password-reset__form" @submit.prevent.stop="resetPassword">
            <UIInput
                class="password-reset__field"
                placeholder="Новый пароль"
                type="password"
                v-model="passwordData.password1"
            />
            <UIInput
                class="password-reset__field"
                placeholder="Повторить пароль"
                type="password"
                v-model="passwordData.password2"
            />
            <UIButton class="password-reset__button">Сохранить</UIButton>
        </form>
    </div>
</template>

<style lang="scss" scoped>
    .password-reset {
        min-height: 70vh;
        display: flex;
        align-items: center;
        justify-content: center;
        &__form {
            margin-top: clampFluid(24);
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            gap: clampFluid(20);
            @include tablet {
                margin-top: 12px;
                gap: 15px;
            }
        }
        &__field {
            width: 100%;
        }
    }
</style>
