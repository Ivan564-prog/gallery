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
                <UIImage class="account-link__image" />
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
</style>