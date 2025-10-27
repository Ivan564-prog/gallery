<script lang="ts" setup>
    const route = useRoute()
    const { data: registrationStatus } = await useRequest<IRegistrationStatus>('/api/v1/user/check_register/', 'GET', {
        code: route.query.code,
    })
</script>

<template>
    <div class="registration">
        <div class="registration__info">
            <template v-if="registrationStatus.success">
                <h2 class="registration__info-title h1">Добро пожаловать!</h2>
                <p class="registration__info-text p2">Вы получили приглашение присоединиться <br> к миссионерскому отделу</p>
            </template>
            <template v-else>
                <h2 class="registration__info-title h1">Ошибка!</h2>
                <p class="registration__info-text p2">Проверьте, что ссылка верна и не устарела.</p>
            </template>
        </div>
        <div v-if="registrationStatus.success" class="registration__wrapper">
            <RegistrationDioceseForm v-if="registrationStatus.role === 'admin'" class="registration__form" />
            <RegistrationUserForm v-else />
        </div>
    </div>
</template>

<style lang="scss" scoped>
    .registration {
        display: grid;
        grid-template-columns: clampFluid(743) 1fr;
        gap: clampFluid(143);
        height: calc(100dvh - clampFluid(20));
        @include tablet {
            grid-template-columns: 1fr;
        }
        &__info {
            position: relative;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: clampFluid(16);
            text-align: center;
            padding: clampFluid(122) clampFluid(40);
            &:before {
                content: '';
                position: absolute;
                z-index: -1;
                inset: 0;
                background-color: var(--gray-06);
            }
        }
        &__wrapper {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
            padding: clampFluid(122) clampFluid(40);
            @include tablet {
                padding: 0 20px 56px;
            }
        }
        &__form {
            max-width: 743px;
            width: 100%;
        }
    }
</style>