<script lang="ts" setup>
    const { type = 'text' } = defineProps<{
        type?: 'text' | 'tel' | 'password'
        errorText?: string,
    }>()
</script>

<template>
    <UIInputText 
        v-if="type == 'text'" 
        :error-text="errorText"
    />
    <UIInputPhone 
        v-else-if="type == 'tel'" 
        :error-text="errorText"
    />
    <UIInputPassword 
        v-else-if="type == 'password'" 
        :error-text="errorText"
    />
</template>

<style lang="scss" scoped></style>
