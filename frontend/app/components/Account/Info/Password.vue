<script lang="ts" setup>
    const userID = useCookie('user-id')
    const toastrStore = useToastrStore()
    const params = reactive({
        password1: '',
        password2: '',
    })
    const errorInfo = ref<IPasswordErrors & IUserErrors>({})

    const setPassword = async () => {
        errorInfo.value = {}

        if (params.password1 !== params.password2) {
            toastrStore.showError('Пароли не совпадают')
            return
        }

        try {
            await request<IUser>(`/api/v1/user/${userID.value}/`, 'PATCH', {
                password: params.password1,
            })
            toastrStore.showSuccess('Пароль успешно обновлен')
            Object.keys(params).forEach(key => ((params as any)[key] = ''))
        } catch (error) {
            const errorMessage = (error as IHttpError<IPasswordErrors>).data.nonFieldErrors
            if (errorMessage?.length) toastrStore.showError(errorMessage[0]!)
            errorInfo.value = (error as IHttpError<IUserErrors>).data
        }
    }
</script>

<template>
    <form class="account-password" @submit.prevent="setPassword">
        <div class="account-password__fields">
            <AccountInfoContactsItem
                placeholder="Придумайте новый пароль"
                title="Изменить пароль"
                type="password"
                :error-text="errorInfo.password1 && errorInfo.password1[0]"
                v-model="params.password1"
            />
            <AccountInfoContactsItem
                placeholder="Повторите пароль"
                type="password"
                v-model="params.password2"
            />
        </div>
        <UIButton class="account-password__button" size="small" color-variant="gray">
            Сохранить новый пароль
        </UIButton>
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
