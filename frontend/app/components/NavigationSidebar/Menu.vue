<script lang="ts" setup>
    const route = useRoute()
    const menuList = computed(() => [
            {
                id: 1,
                name: 'Библиотека',
                icon: 'library',
                link: '/library',
            },
        ])
</script>

<template>
    <nav class="navigation-menu">
        <UILink
            v-for="item in menuList"
            class="navigation-menu__item menu-item"
            :key="item.id"
            :to="item.link"
            :class="{
                'menu-item--active': route.path === item.link,
            }"
        >
            <NuxtIcon class="menu-item__icon" :name="item.icon" />
            <span class="menu-item__title p2">{{ item.name }}</span>
            <p v-if="item.count" class="menu-item__count p4">{{ item.count }}</p>
        </UILink>
    </nav>
</template>

<style lang="scss" scoped>
    .navigation-menu {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        gap: clampFluid(17);
        @include mobile {
            flex-direction: row;
        }
    }

    .menu-item {
        $this: &;
        position: relative;
        display: flex;
        align-items: center;
        gap: clampFluid(20);
        padding: clampFluid(11) clampFluid(40);
        @include mobile {
            flex-direction: column;
            gap: 6px;
            padding: 9px 0 6px;
        }
        &::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            width: clampFluid(6);
            height: 100%;
            background-color: var(--color);
            opacity: 0;
            transition: $tr;
            @include mobile {
                top: auto;
                bottom: 0;
                width: 100%;
                height: 3px;
            }
        }
        &--active {
            &:before {
                opacity: 1;
            }
            #{$this}__icon {
                color: var(--black);
            }
            #{$this}__title {
                color: var(--black);
            }
        }
        &__icon {
            flex: 0 0 auto;
            width: clampFluid(35);
            height: auto;
            aspect-ratio: 1;
            color: var(--gray-03);
            transition: $tr;
        }
        &__title {
            color: var(--gray-02);
            transition: $tr;
            @include tablet {
                font-size: 0;
            }
            @include mobile {
                font-size: 10px;
            }
        }
        &__count {
            display: flex;
            align-items: center;
            justify-content: center;
            margin-left: auto;
            width: clampFluid(28);
            height: auto;
            aspect-ratio: 1;
            border-radius: 100%;
            background-color: var(--color);
            color: var(--white);
            @include tablet {
                position: absolute;
                top: 0;
                right: 0;
            }
        }
    }
</style>
