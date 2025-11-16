<script lang="ts" setup>
</script>

<template>
    <div class="registration">
        <div class="registration__info">
            <h2 class="registration__info-title h1">Добро пожаловать!</h2>
            <p class="registration__info-text p2">В музей изобразительных искусств</p>
        </div>
        <div class="registration__wrapper">
            <RegistrationUserForm class="registration__form" />
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
            gap: 40px;
        }
        &__info {
            position: relative;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            align-items: center;
            gap: clampFluid(16);
            text-align: center;
            padding: clampFluid(240) clampFluid(40);
            @include tablet {
                padding: 90px 20px;
            }
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