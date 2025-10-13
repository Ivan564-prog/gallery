<script lang="ts" setup>
    defineProps<{
        breadcrumbList: IBreadcrumb[]
    }>()
</script>

<template>
    <div class="ui-breadcrumbs">
        <SchemaBreadcrumbs :breadcrumbs="breadcrumbList" />
        <div class="ui-breadcrumbs__container container">
            <UILink to="/" class="ui-breadcrumbs__item ui-breadcrumb-item ui-breadcrumb-item--link">
                Главная
            </UILink>
            <template v-for="item in breadcrumbList">
                <NuxtLink
                    v-if="item.link"
                    :to="item.link"
                    class="ui-breadcrumbs__item ui-breadcrumb-item ui-breadcrumb-item--link"
                >
                    {{ item.title }}
                </NuxtLink>
                <p v-else class="ui-breadcrumbs__item ui-breadcrumb-item">
                    {{ item.title }}
                </p>
            </template>
        </div>
    </div>
</template>

<style lang="scss" scoped>
    .ui-breadcrumbs {
        &__container,
        &__item {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }
    }
    .ui-breadcrumb-item {
        color: rgba(#000, 0.5);
        @include p1;
        &:not(:first-child) {
            &::before {
                content: '/';
                font-weight: 400;
                font-size: 14px;
                line-height: 130%;
                letter-spacing: 0.02em;
            }
        }
        &__icon {
            width: 16px;
            height: auto;
            aspect-ratio: 1;
            color: #000;
        }
        &--link {
            transition: all 0.3s ease;
            @include hover {
                color: #000;
                .nuxt-icon {
                    color: #000;
                }
            }
        }
    }
</style>
