<script lang="ts" setup>
    const { 
        to, 
        widthMode = 'auto',
        variant = 'default',
        fontSize = 'default',
    } = defineProps<{
        to?: string
        widthMode?: 'full' | 'auto'
        variant?: 'default' | 'gray' | 'empty-red' | 'empty-black'
        fontSize?: 'default' | 'big'
    }>()

    const nuxtLink = resolveComponent('UILink')
    const tag = computed(() => {
        if (to) return nuxtLink
        else return 'button'
    })
</script>

<template>
    <component 
        class="ui-button" 
        :is="tag" 
        :to="to" 
        :class="`
            ui-button--width-${widthMode} 
            ui-button--variant-${variant} 
        `"
    >
        <span 
            class="ui-button__text"
            :class="`ui-button__text--size-${fontSize}`"
        >
            <slot></slot>
        </span>
    </component>
</template>

<style lang="scss" scoped>
    .ui-button {
        $this: &;
        display: flex;
        justify-content: center;
        align-items: center;
        height: clampFluid(59);
        padding: 0 15px;
        background-color: var(--background-color);
        border: 2px solid var(--border-color);
        transition: $tr;
        @include hover {
            background-color: var(--color-hover);
            #{$this}__text {
                color: var(--white);
            }
        }
        &--width {
            &--full {
                width: 100%;
            }
            &--auto {
                width: fit-content;
            }
        }
        &--variant {
            &-default {
                --background-color: var(--color);
                --border-color: var(--color);
                --font-color: var(--white);
            }
            &-gray {
                --background-color: var(--gray_05);
                --border-color: var(--gray_05);
                --font-color: var(--black);
            }
            &-empty-red {
                --background-color: transparent;
                --border-color: var(--gray_05);
                --font-color: var(--black);
            }
            &-empty-black {
                --background-color: transparent;
                --border-color: var(--black);
                --font-color: var(--black);
            }
        }
        &__text {
            color: var(--black);
            transition: $tr;
        }
    }
</style>
