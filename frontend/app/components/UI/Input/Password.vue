<script lang="ts" setup>
    const modelValue = defineModel<string | number>()
    defineProps<{
        styleVariant?: 'default' | 'minimal' | 'big'
        placeholder?: string
        errorText?: string
    }>()
    const type = ref<'text' | 'password'>('password')
    const toggleSecret = () => {
        type.value = type.value == 'text' ? 'password' : 'text'
    }
</script>

<template>
    <div class="ui-input-password">
        <UIInputBase 
            :type="type" 
            :placeholder="placeholder" 
            :error-text="errorText"
            :style-variant="styleVariant"
            v-model="modelValue"
        />
        <button 
            class="ui-input-password__toggle" 
            type="button"
            @click="toggleSecret"
        >
            <NuxtIcon 
                class="ui-input-password__icon" 
                name="eye" 
                :class="{
                    'ui-input-password__icon--active': type === 'text',
                }"
            />
        </button>
    </div>
</template>

<style lang="scss" scoped>
    .ui-input-password {
        position: relative;
        &__toggle {
            height: 100%;
            width: auto;
            aspect-ratio: 1;
            position: absolute;
            right: 0;
            top: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
        }
        &__icon {
            width: clampFluid(24);
            height: auto;
            aspect-ratio: 1;
            color: var(--black);
            transition: $tr;
            &--active {
                color: var(--color);
            }
        }
    }
</style>
