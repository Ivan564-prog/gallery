<script lang="ts" setup>
    
</script>

<template>
    <section class="reset-password">
        <UILink class="reset-password__back-link back-link" to="/login">
            <NuxtIcon class="back-link__icon" name="arrow" />
            <span class="back-link__text p2 p2--bold">Вернуться назад</span>
        </UILink>
        <ResetPasswordForm class="reset-password__form" />
        <Teleport to="body">
            <ResetPasswordSuccess />
        </Teleport>
    </section>
</template>

<style lang="scss" scoped>
    .reset-password {
        padding: 0 clampFluid(20, 60);
        &__back-link {
            margin-top: clampFluid(61);
        }
        &__form {
            width: 100%;
            max-width: clampFluid(600);
            margin: clampFluid(124) auto 0;
            @include tablet {
                margin: 40px auto 0;
            }
        }
    }

    .back-link {
        display: inline-flex;
        align-items: center;
        gap: clampFluid(20);
        color: var(--gray-02);
        transition: $tr;
        @include hover {
            color: var(--color);
        }
        &__icon {
            width: clampFluid(16);
            height: auto;
            aspect-ratio: 16 / 9;
            rotate: 90deg;
        }
    }
</style>