<script lang="ts" setup>
    const {
        variant = 'center',
    } = defineProps<{
        icon: string
        text: string
        variant?: 'center' | 'flex-start'
        errorText?: string
    }>()
</script>

<template>
    <div 
        class="titled-input" 
        :style="{
            'align-items': variant,
        }"
    >
        <div class="titled-input__content">
            <NuxtIcon class="titled-input__content-icon" :name="icon" />
            <span 
                class="titled-input__content-text p2"
                :class="{
                    'titled-input__content-text--error': errorText,
                }"
            >{{ text }}</span>
        </div>
        <div class="titled-input__field">
            <slot></slot>
        </div>
    </div>
</template>

<style lang="scss" scoped>
    .titled-input {
        display: grid;
        grid-template-columns: clampFluid(265) 1fr;
        gap: clampFluid(24);
        @include tablet {
            grid-template-columns: 1fr;
            gap: 8px;
        }
        &__content {
            display: flex;
            align-items: center;
            gap: clampFluid(16);
        }
        &__content-icon {
            flex: 0 0 auto;
            width: clampFluid(24);
            height: auto;
            aspect-ratio: 1;
            color: var(--gray-03);
        }
        &__content-text {
            &--error {
                color: var(--color);
            }
        }
    }
</style>