<script lang="ts" setup>
    const modelValue = defineModel<string | number>()
    const input = defineModel<HTMLInputElement>('input')
    const { 
        type = 'text', 
        readonly = false,
        styleVariant = 'default',
    } = defineProps<{
        type?: 'text' | 'number' | 'password'
        placeholder?: string
        readonly?: boolean
        styleVariant: 'default' | 'minimal' | 'big'
    }>()
</script>

<template>
    <label 
        class="ui-input"
        :class="`ui-input--variant-${styleVariant}`"
    >
        <input
            class="ui-input__value"
            placeholder=" "
            ref="input"
            :type="type"
            :readonly="readonly"
            v-model.trim="modelValue"
        />
        <span v-if="placeholder" class="ui-input__placeholder">
            {{ placeholder }}
        </span>
    </label>
</template>

<style lang="scss" scoped>
    .ui-input {
        $this: &;
        position: relative;
        cursor: text;
        display: flex;
        align-items: center;
        width: 100%;
        &:not(:has(#{$this}__value:placeholder-shown)),
        &:has(#{$this}__value:focus-visible) {
            #{$this}__placeholder {
                opacity: 0;
            }
        }
        &--variant {
            &-default {
                border: 1px solid var(--gray-04);
                padding: 0 clampFluid(20);
                height: clampFluid(59);
            }
            &-minimal {
                padding: clampFluid(4) clampFluid(16);
                border-bottom: 1px solid var(--gray-04);
            }
            &-big {
                #{$this}__value,
                #{$this}__placeholder {
                    @include h3;
                }
            }
        }
        &__value {
            @include p2;
            & {
                width: 100%;
                height: 100%;
                border: none;
            }
            &::placeholder {
            }
        }
        &__placeholder {
            @include p2;
            & {
                position: absolute;
                color: var(--gray-03) !important;
                transition: $tr;
            }
        }
    }
</style>
