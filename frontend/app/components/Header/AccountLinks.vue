<script lang="ts" setup>
    const userStore = useUserStore()
    const wishListStore = useWishlistStore()
    const socialList = computed(() => {
        if (userStore.userData?.role == 'root')
            return [
                { id: 1, icon: 'hearth', link: '/favorites', count: 1, },
                { id: 2, icon: 'bell', link: '/notifications', count: 1, },
            ]
        else if (userStore.userData?.role == 'missionary')
             return [
                { id: 1, icon: 'hearth', link: '/favorites', count: 1, },
                { id: 2, icon: 'bell', link: '/notifications', count: 1, },
            ]
        else 
            return [
                { id: 1, icon: 'star', link: '/report', count: 1, },
                { id: 2, icon: 'hearth', link: '/favorites', count: 1, },
                { id: 3, icon: 'bell', link: '/notifications', count: 1, },
            ]

    })
</script>

<template>
    <nav class="account-links">
        <UIButton 
            v-if="userStore.userData?.role == 'missionary'" 
            class="account-links__add-post-button"
        >Новая запись</UIButton>
        <div class="account-links__list">
            <UILink 
                v-for="item in socialList"
                class="account-links__item account-link"
                :key="item.id"
                :to="item.link"
            >
                <NuxtIcon class="account-link__icon" :name="item.icon" />
                <p class="account-link__count p4">{{ item.count }}</p>
            </UILink>
            <UILink 
                class="account-link account-link--personal-account"
                to="/account"
            >
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