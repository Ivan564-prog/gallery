<script lang="ts" setup>
    const userStore = useUserStore()
</script>

<template>
    <nav class="account-links">
        <div class="account-links__list">
            <UILink class="account-link account-link--personal-account" to="/">
                <UIImage class="account-link__image" :src="userStore.userData?.image" />
            </UILink>
        </div>
    </nav>
</template>

<style lang="scss" scoped>
    .account-links {
        display: flex;
        align-items: center;
        gap: clampFluid(30);
        &__list {
            display: flex;
            align-items: center;
            gap: clampFluid(13);
        }
    }

    .account-link {
        $this: &;
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        width: clampFluid(62);
        height: auto;
        aspect-ratio: 1;
        border-radius: 50%;
        background-color: var(--gray-06);
        transition: $tr;
        @include hover {
            background-color: var(--gray-05);
            #{$this}__icon {
                color: var(--color);
            }
        }
        &--personal-account {
            overflow: hidden;
        }
        &__icon {
            width: clampFluid(40);
            height: auto;
            aspect-ratio: 1;
            color: var(--gray-01);
            transition: $tr;
        }
        &__image {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        &__count {
            position: absolute;
            top: 0;
            right: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            translate: 25% -25%;
            width: clampFluid(28);
            height: auto;
            aspect-ratio: 1;
            border-radius: 50%;
            background-color: var(--color);
            color: var(--white);
        }
    }
</style>
