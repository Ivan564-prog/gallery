<script lang="ts" setup>
    const userStore = useUserStore()
    const { data: typeList } = await useRequest<IBookType[]>('/api/v1/library/book_type/')
    const bookType = defineModel<number>()
</script>

<template>
    <div class="library-head">
        <div class="library-head__filters">
            <label class="library-head__filter library-filter">
                <span class="library-filter__text p2 p2--bold">Все материалы</span>
                <input 
                    class="library-filter__radio" 
                    name="library-type"
                    type="radio"
                    :value="undefined"
                    v-model="bookType"
                />
            </label>
            <label class="library-head__filter library-filter">
                <span class="library-filter__text p2 p2--bold">Сохраненные</span>
                <NuxtIcon class="library-filter__icon" name="favorite-2" />
                <input 
                    class="library-filter__radio" 
                    name="library-type"
                    type="radio"
                    :value="-1"
                    v-model="bookType"
                />
            </label>
            <label 
                v-for="type in typeList"
                class="library-head__filter library-filter"
                :key="type.id"
            >
                <span class="library-filter__text p2 p2--bold">{{ type.title }}</span>
                <input 
                    class="library-filter__radio" 
                    name="library-type"
                    type="radio"
                    :value="type.id"
                    v-model="bookType"
                />
            </label>
        </div>
        <!-- TODO ДОБАВИТЬ КОГДА ЗАКОНЧУ v-if="userStore.userData?.role === 'root'" -->
        <UIButton 
            class="library-head__button"
            to="#book-creator"
        >Добавить публикацию</UIButton>
    </div>
</template>

<style lang="scss" scoped>
    .library-head {
        display: flex;
        align-items: center;
        justify-content: space-between;
        &__filters {
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: clampFluid(14);
        }
    }

    .library-filter {
        $this: &;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: clampFluid(20);
        height: clampFluid(59);
        background-color: var(--gray-05);
        border: 2px solid var(--gray-05);
        transition: $tr;
        @include hover {
            color: var(--white);
            background-color: var(--color-hover);
            border-color: var(--color-hover);
            #{$this}__icon {
                color: var(--white);
            }
        }
        &:has(#{$this}__radio:checked) {
            color: var(--black);
            pointer-events: none;
            background-color: transparent;
            border-color: var(--color);
            #{$this}__icon {
                color: var(--color);
            }
        }
        &__icon {
            width: clampFluid(40);
            height: auto;
            aspect-ratio: 1;
            color: var(--color);
            transition: $tr;
        }
        &__radio {
            display: none;
        }

    }
</style>