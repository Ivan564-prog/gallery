<script lang="ts" setup>
    defineProps<{
        typeList: IBookType[]
    }>()
    const userStore = useUserStore()
    const query = defineModel<string>()
</script>

<template>
    <div class="library-head">
        <WidgetSearch class="library-head__search" v-model="query" />
        <UIButton
            v-if="userStore.userData?.role === 'admin'"
            class="library-head__button"
            to="#book-creator"
        >Добавить картину</UIButton>
    </div>
</template>

<style lang="scss" scoped>
    .library-head {
        display: flex;
        align-items: center;
        justify-content: space-between;
        @include mobile {
            flex-direction: column;
            align-items: baseline;
            gap: 20px;
        }
        &__search {
            @include mobile {
                width: 100%;
            }
        }
        &__button {
            @include mobile {
                position: fixed;
                z-index: 5;
                bottom: 70px;
                left: 20px;
                right: 20px;
                width: auto;
            }
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
