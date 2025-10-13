<script lang="ts" setup>
    const page = defineModel<number>('page', { default: 1 })
    const { maxPage } = defineProps<{
        maxPage: number
    }>()

    watch(
        () => maxPage,
        () => {
            if (maxPage < page.value) page.value = maxPage
        },
    )
    const aroundExt = 2
    const aroundActive = 2
    if (page.value > maxPage) page.value = maxPage

    const setPage = (val: number) => {
        page.value = val
    }
</script>

<template>
    <div class="pagination" v-if="maxPage > 1">
        <button
            class="pagination-button pagination-button--prev"
            :class="page <= 1 && 'pagination-button--disable'"
            @click="() => page--"
        >
            <NuxtIcon class="pagination-button__icon" name="slider-arrow" />
        </button>
        <div class="pagination__list">
            <template v-for="p in aroundExt + 1">
                <button class="pagination-item" v-if="maxPage >= p && p != page" @click="setPage(p)">
                    {{ p }}
                </button>
                <div class="pagination-item pagination-item--active" v-else-if="maxPage >= p && p == page">
                    {{ p }}
                </div>
            </template>
            <div class="pagination-item" v-if="aroundExt + 2 < page - aroundActive">...</div>
            <template v-for="p in aroundActive * 2 + 1">
                <button
                    class="pagination-item"
                    v-if="
                        page + p - 1 - aroundActive > aroundExt + 1 &&
                        page + p - 1 - aroundActive <= maxPage &&
                        page != page + p - 1 - aroundActive
                    "
                    @click="setPage(page + p - 1 - aroundActive)"
                >
                    {{ page + p - 1 - aroundActive }}
                </button>
                <div
                    class="pagination-item pagination-item--active"
                    v-else-if="
                        page + p - 1 - aroundActive > aroundExt + 1 &&
                        page + p - 1 - aroundActive <= maxPage &&
                        page == page + p - 1 - aroundActive
                    "
                >
                    {{ page + p - 1 - aroundActive }}
                </div>
            </template>
            <div class="pagination-item" v-if="maxPage - aroundExt > page + aroundActive + 1">...</div>
            <template v-for="p in aroundExt + 1">
                <div
                    class="pagination-item"
                    v-if="
                        maxPage + p - 1 - aroundExt >= page + aroundActive + 1 &&
                        page != maxPage + p - 1 - aroundExt
                    "
                    @click="setPage(maxPage + p - 1 - aroundExt)"
                >
                    {{ maxPage + p - 1 - aroundExt }}
                </div>
                <div
                    class="pagination-item pagination-item--active"
                    v-else-if="
                        maxPage + p - 1 - aroundExt >= page + aroundActive + 1 &&
                        page == maxPage + p - 1 - aroundExt
                    "
                >
                    {{ maxPage + p - 1 - aroundExt }}
                </div>
            </template>
        </div>
        <button
            class="pagination-button pagination-button--next"
            :class="page >= maxPage && 'pagination-button--disable'"
            @click="() => page++"
        >
            <NuxtIcon class="pagination-button__icon" name="slider-arrow" />
        </button>
    </div>
</template>

<style lang="scss" scoped>
    .pagination {
        display: flex;
        align-items: center;
        gap: clampFluid(30);
        &__list {
            display: flex;
            gap: 10px;
        }
    }

    .pagination-item {
        width: clampFluid(64);
        height: auto;
        aspect-ratio: 1;
        border: 2px solid transparent;
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        opacity: 0.7;
        @include p1;
        &--active {
            opacity: 1;
            pointer-events: none;
            border-color: var(--color-main);
        }
    }

    .pagination-button {
        width: clampFluid(64);
        height: auto;
        aspect-ratio: 1;
        background-color: var(--white);
        display: flex;
        align-items: center;
        justify-content: center;
        &--disable {
            opacity: 0.5;
            pointer-events: none;
        }
        &--prev {
            rotate: 180deg;
        }
        &__icon {
            width: clampFluid(24);
            height: auto;
            aspect-ratio: 24 / 18;
            color: var(--black);
        }
    }
</style>
