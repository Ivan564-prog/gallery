<script lang="ts" setup>
    const { type = 'text' } = defineProps<{
        type?: 'text' | 'tel' | 'password' | 'date'
        errorText?: string,
    }>()
</script>

<template>
    <UIInputPhone 
        v-if="type == 'tel'" 
        :type="type"
        :error-text="errorText"
    />
    <UIInputPassword 
        v-else-if="type == 'password'" 
        :type="type"
        :error-text="errorText"
    />
    <UIInputText 
        v-else 
        :type="type"
        :error-text="errorText"
    />
</template>

<style lang="scss" scoped></style>
