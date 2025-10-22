<script lang="ts" setup>
    const route = useRoute()
    const isActualLink = ref<boolean>()
    
    const setActualLink = async () => {
        const resetPasswordStatus = await request<boolean>(
            '/api/v1/user/check_reset/', 
            'GET', 
            route.query
        )
        isActualLink.value = resetPasswordStatus
    }
    setActualLink()
</script>

<template>
    <section class="reset-password">
        <ResetPasswordForm 
            v-if="isActualLink" 
            class="reset-password__form" 
        />
        <UIEmptyBanner 
            v-else="isActualLink === false" 
            title="Не удалось подтвердить активацию. Проверьте, что ссылка верна и не устарела." 
        />
        <Teleport to="body">
            <ResetPasswordSuccess />
        </Teleport>
    </section>
</template>

<style lang="scss" scoped>
    .reset-password {
        padding: 0 clampFluid(20, 60);
        &__form {
            width: 100%;
            max-width: clampFluid(600);
            margin: clampFluid(124) auto 0;
            @include tablet {
                margin: 40px auto 0;
            }
        }
    }
</style>