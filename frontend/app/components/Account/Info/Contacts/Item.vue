<script lang="ts" setup>
    const value = defineModel<string>({ required: true })
    const { readonly = false, type = 'text' } = defineProps<{
        title?: string
        readonly?: boolean
        placeholder?: string
        type?: 'text' | 'tel' | 'password' | 'date'
        errorText?: string
    }>()
</script>

<template>
    <div class="contact-item">
        <p class="contact-item__title p3">{{ title }}</p>
        <UIInput
            class="contact-item__field"
            style-variant="minimal"
            :readonly="readonly"
            :placeholder="placeholder"
            :type="type"
            :error-text="errorText"
            v-model="value"
        />
    </div>
</template>

<style lang="scss" scoped>
    .contact-item {
        display: grid;
        grid-template-columns: clampFluid(240) 1fr;
        align-items: center;
        gap: clampFluid(20);
        @include tablet {
            grid-template-columns: 1fr;
            align-items: flex-start;
            gap: 8px;
        }
        &__title {
            color: var(--gray-03);
        }
    }
</style>
