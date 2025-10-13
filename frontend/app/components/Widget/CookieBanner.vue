<script lang="ts" setup>
    const isShowingCookie = useCookie<boolean>('cookie-accept', {
        default: () => true,
    })
    const isOpened = ref<boolean>(isShowingCookie.value)

    const closeBanner = () => {
        isShowingCookie.value = false
        isOpened.value = false
    }
</script>

<template>
    <Transition name="cookie">
        <div v-if="isOpened" class="cookie-banner">
            <div class="cookie-banner__wrapper">
                <div class="cookie-banner__content">
                    <p class="cookie-banner__text p1">Мы собираем cookies для корректной работы сайта.</p>
                    <UILink to="/privacy-policy" class="cookie-banner__link p1">
                        Политика конфиденциальности
                    </UILink>
                </div>
                <UIButton @click="closeBanner">Хорошо</UIButton>
            </div>
        </div>
    </Transition>
</template>

<style lang="scss" scoped>
    .cookie-banner {
        position: fixed;
        z-index: 5;
        translate: -50% 0;
        left: 50%;
        bottom: clampFluid(7);
        max-width: clampFluid(1470);
        width: 100%;
        padding: clampFluid(13) clampFluid(30);
        background-color: #fff;
        @include tablet {
            left: 0;
            right: 0;
            bottom: 5px;
            translate: 0 0;
            padding: 20px;
        }
        &.cookie-enter-active,
        &.cookie-leave-active {
            transition: 0.3s;
        }
        &.cookie-enter-from,
        &.cookie-leave-to {
            opacity: 0;
            translate: -50% 100%;
        }
        &__wrapper {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 16px;
            @include tablet {
                flex-direction: column;
            }
        }
        &__content {
            display: flex;
            gap: clampFluid(5);
            @include tablet {
                text-align: center;
                align-items: center;
                flex-direction: column;
            }
        }
        &__link {
            color: #3500f5;
            text-decoration: underline;
            text-decoration-skip-ink: none;
            @include hover {
                text-decoration: none;
            }
        }
    }
</style>
