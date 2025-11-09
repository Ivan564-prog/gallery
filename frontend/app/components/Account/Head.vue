<script lang="ts" setup>
    const currentTab = defineModel<number>({ required: true })
    const confirmStore = useConfirmStore()
    const userStore = useUserStore()
    const tabList = computed(() => {
        switch (userStore.userData?.role) {
            case 'chief':
                return [
                    { id: 1, title: 'Мои данные' },
                    { id: 2, title: 'Приглашенные пользователи' },
                ]
            case 'root':
                return [
                    { id: 1, title: 'Мои данные' },
                    { id: 2, title: 'Приглашенные администрации' },
                ]
            default:
                return [
                    { id: 1, title: 'Мои данные' },
                    { id: 2, title: 'Активные пользователи' },
                ]
        }
    })

    const logout = async () => {
        try {
            await confirmStore.openConfirmModal('Подтверждение', 'Вы действительно хотите выйти из аккаунта?')
            await request('/api/v1/user/logout/', 'POST')
            navigateTo('/login')
        } catch {
            return
        }
    }
</script>

<template>
    <div class="account-head">
        <div class="account-head__tabs">
            <div class="account-head__tabs-list">
                <h3 class="account-head__title h3">Данные пользователя</h3>
            </div>
        </div>
        <button class="account-head__logout-button logout-button" @click="logout">
            <span class="logout-button__text p2">Выйти из аккаунта</span>
            <NuxtIcon class="logout-button__icon" name="logout" />
        </button>
    </div>
</template>

<style lang="scss" scoped>
    .account-head {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: clampFluid(20);
        @include tablet {
            align-items: flex-start;
            flex-direction: column-reverse;
        }
        &__tabs {
            overflow: auto;
            @include tablet {
                width: calc(100dvw - 40px);
            }
        }
        &__tabs-list {
            display: flex;
            align-items: center;
            gap: clampFluid(50);
            width: fit-content;
            @include tablet {
                gap: 30px;
            }
        }
        &__tab {
            position: relative;
            overflow: hidden;
            padding-bottom: clampFluid(15);
            white-space: nowrap;
            transition: $tr;
            @include hover {
                color: var(--color);
            }
            &:before {
                content: '';
                position: absolute;
                left: -100%;
                bottom: 0;
                width: 100%;
                height: 2px;
                background-color: var(--color);
                transition: $tr;
            }
            &--active {
                pointer-events: none;
                &::before {
                    left: 0;
                }
            }
        }
        &__logout-button {
            margin-bottom: clampFluid(15);
        }
    }

    .logout-button {
        display: flex;
        align-items: center;
        gap: clampFluid(12);
        color: var(--gray-02);
        transition: $tr;
        @include hover {
            color: var(--color);
        }
        &__icon {
            width: clampFluid(30);
            height: auto;
            aspect-ratio: 1;
            @include tablet {
                width: 30px;
            }
        }
    }
</style>
