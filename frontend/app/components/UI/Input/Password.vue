<script lang="ts" setup>
    const modelValue = defineModel<string | number>()
    defineProps<{
        placeholder?: string
    }>()
    const type = ref<'text' | 'password'>('password')
    const toggleSecret = () => {
        type.value = type.value == 'text' ? 'password' : 'text'
    }
</script>

<template>
    <div class="ui-input-password">
        <UIInputBase :type="type" v-model="modelValue" :placeholder="placeholder" />
        <div class="ui-input-password__toggle" @click="toggleSecret">
            <NuxtIcon name="eye" />
        </div>
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
            .nuxt-icon {
                width: 20px;
                height: auto;
                aspect-ratio: 1;
            }
        }
    }
</style>
