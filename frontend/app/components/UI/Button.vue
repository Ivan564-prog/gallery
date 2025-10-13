<script lang="ts" setup>
    const { to, widthMode = 'auto' } = defineProps<{
        to?: string
        widthMode?: 'full' | 'auto'
    }>()

    const nuxtLink = resolveComponent('UILink')
    const tag = computed(() => {
        if (to) return nuxtLink
        else return 'button'
    })
</script>

<template>
    <component :is="tag" :to="to" class="ui-button" :class="`ui-button--width-${widthMode}`">
        <span class="ui-button__text">
            <slot></slot>
        </span>
    </component>
</template>

<style lang="scss" scoped>
    .ui-button {
        display: flex;
        justify-content: center;
        align-items: center;
        user-select: none;
        cursor: pointer;
        transition: all 0.3s ease;
        border: none;
        height: 47px;
        padding: 0 15px;
        background-color: $main-clr;
        &--width {
            &--full {
                width: 100%;
            }
            &--auto {
                width: fit-content;
            }
        }
        &__text {
            color: #fff;
        }
    }
</style>
