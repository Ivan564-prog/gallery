<script lang="ts" setup>
    const {
        sizeVariant = 'big'
    } = defineProps<{
        sizeVariant?: 'big' | 'small'
    }>()
    const modelValue = defineModel<boolean>()
</script>

<template>
    <label class="ui-checkbox">
        <input class="ui-checkbox__input" type="checkbox" v-model="modelValue" />
        <div 
            class="ui-checkbox__marker"
            :class="`ui-checkbox__marker--size-${sizeVariant}`"
        >
            <NuxtIcon class="ui-checkbox__marker-icon" name="mark" />
        </div>
        <span class="ui-checkbox__text">
            <slot></slot>
        </span>
    </label>
</template>

<style lang="scss" scoped>
    .ui-checkbox {
        $this: &;
        display: flex;
        gap: 10px;
        width: fit-content;
        align-items: baseline;
        cursor: pointer;
        &__input {
            display: none;
            &:checked {
                & ~ #{$this}__marker {
                    &::after {
                        background-color: var(--gray-03);
                    }
                    #{$this}__marker-icon {
                        opacity: 1;
                    }
                }
            }
        }
        &__marker {
            position: relative;
            border: 1px solid var(--gray-03);
            display: block;
            height: auto;
            aspect-ratio: 1;
            &::after {
                content: '';
                width: 100%;
                height: 100%;
                display: flex;
            }
            &--size {
                &-big {
                    width: clampFluid(27);
                }
                &-small {
                    width: clampFluid(24);
                }
            }
        }
        &__marker-icon {
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            color: var(--black);
            opacity: 0;
        }
        &__text {
        }
    }
</style>
