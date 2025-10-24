<script lang="ts" setup>
    const modelValue = defineModel<IDioceseExtend>({ required: true })
    const toastrStore = useToastrStore()
    const inviteParams = reactive({
        diocese: modelValue.value.id,
        email: '',
    })

    const sendInvite = async () => {
        try {
            const response = await request<IInviteResponse>('/api/v1/user/invite/', 'POST', inviteParams)
            modelValue.value = {
                ...modelValue.value,
                ...(response.status === 'created'
                    ? { invite: response.invite! }
                    : {
                          id: response.user?.id!,
                          image: response.user?.image || null,
                          email: response.user?.email!,
                      }),
            }
            toastrStore.showSuccess(response.message)
        } catch {
            toastrStore.showError('Ошибка приглашения')
        }
    }

    const removeInvite = async () => {
        try {
            await request<IInviteResponse>(`/api/v1/user/invite/${modelValue.value.invite?.id}/`, 'DELETE')
            modelValue.value = {
                ...modelValue.value,
                invite: null,
            }
            toastrStore.showSuccess('Приглашение успешно удалено')
        } catch {
            toastrStore.showError('Приглашение не найдено')
        }
    }

    const removeAdmin = async () => {
        try {
            await request<IInviteResponse>(`/api/v1/user/${modelValue.value.invite?.id}/`, 'DELETE')
            toastrStore.showSuccess('Пользователь успешно удален')
        } catch {
            toastrStore.showError('Не удалось удалить пользователя')
        }
    }
</script>

<template>
    <div class="diocese-item">
        <div class="diocese-item__info">
            <UIImage class="diocese-item__image" :src="modelValue.admin?.image" />
            <p class="diocese-item__title p1 p1--bold">{{ modelValue.title }}</p>
        </div>
        <div v-if="modelValue.invite" class="diocese-item__panel">
            <p class="diocese-item__email p2 p2--bold">{{ modelValue.invite.email }}</p>
            <UIButton class="diocese-item__button" color-variant="empty-black" @click="removeInvite">
                Приглашен
            </UIButton>
        </div>
        <div v-else-if="modelValue.admin" class="diocese-item__panel">
            <p class="diocese-item__email p2 p2--bold">{{ modelValue.admin.email }}</p>
            <UIButton class="diocese-item__button" color-variant="gray" @click="removeAdmin">
                Удалить
            </UIButton>
        </div>
        <form v-else class="diocese-item__panel" @submit.prevent="sendInvite">
            <UIInput class="diocese-item__input" placeholder="Почта" v-model="inviteParams.email" />
            <UIButton class="diocese-item__button">Пригласить</UIButton>
        </form>
    </div>
</template>

<style lang="scss" scoped>
    .diocese-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: clampFluid(20);
        padding: clampFluid(20) 0;
        border-top: 1px solid var(--gray-04);
        @include tablet {
            align-items: flex-start;
            flex-direction: column;
        }
        &__info {
            display: flex;
            align-items: center;
            gap: clampFluid(16);
        }
        &__image {
            flex: 0 0 auto;
            width: clampFluid(50);
            height: auto;
            aspect-ratio: 1;
            border-radius: 50%;
        }
        &__panel {
            display: flex;
            align-items: center;
            gap: clampFluid(20);
            @include tablet {
                width: 100%;
                justify-content: space-between;
            }
        }
        &__input {
            width: clampFluid(442);
            @include tablet {
                flex: 1 1 auto;
                width: auto;
            }
        }
        &__button {
            width: clampFluid(156);
        }
    }
</style>
