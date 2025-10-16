<script lang="ts" setup>
    defineProps<{
        placeholder?: string
    }>()
    const modelValue = defineModel<string>()
</script>

<template>
    <div class="ui-textarea">
        <p v-if="placeholder" class="ui-textarea__placeholder">{{ placeholder }}</p>
        <textarea 
            class="ui-textarea__field" 
            placeholder=""
            v-model="modelValue" 
        ></textarea>
    </div>
</template>

<style lang="scss" scoped>
    .ui-textarea {
        $this: &;
        border: 1px solid var(--gray-04);
        padding: clampFluid(18) clampFluid(30) clampFluid(16) clampFluid(30);
        height: clampFluid(117);
        &:not(:has(#{$this}__field:placeholder-shown)),
        &:has(#{$this}__field:focus-visible) {
            #{$this}__placeholder {
                opacity: 0;
            }
        }
        &__placeholder {
            position: absolute;
            pointer-events: none;
            color: var(--gray-03) !important;
            transition: $tr;
            @include p2;
        }
        &__field {
            border: none;
            resize: none;
            width: 100%;
            height: 100%;
            background-color: transparent;
            @include p2;
        }
    }
</style>
