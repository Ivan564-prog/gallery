<script lang="ts" setup>
    const modelValue = defineModel<string | number>()
    const input = defineModel<HTMLInputElement>('input')
    const { type = 'text' } = defineProps<{
        type?: 'text' | 'number' | 'password'
        placeholder?: string
        readonly?: boolean
    }>()
</script>

<template>
    <label class="ui-input">
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
        border: 1px solid #333;
        cursor: text;
        display: flex;
        align-items: center;
        height: 39px;
        padding: 5px 10px 0;
        font-size: 14px;
        line-height: 125%;
        width: 100%;
        &:not(:has(#{$this}__value:placeholder-shown)),
        &:has(#{$this}__value:focus-visible) {
            #{$this}__placeholder {
                // opacity: 0;
                translate: 0 -1em;
            }
        }
        &__value {
            width: 100%;
            height: 100%;
            border: none;
            font-size: inherit;
            line-height: inherit;

            &::placeholder {
            }
        }
        &__placeholder {
            position: absolute;
            transition: all 0.3s ease;

            font-size: inherit;
            line-height: inherit;
            color: #a3a3a3;
        }
    }
</style>
