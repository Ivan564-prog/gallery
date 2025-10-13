<script lang="ts" setup>
    const modelValue = defineModel<any>()

    const isComponentValid = (blockName: string) => typeof resolveComponent(blockName) === 'string'
</script>

<template>
    <div class="content">
        <template v-for="(_, i) in modelValue" :key="modelValue.id">
            <component
                v-if="isComponentValid(modelValue[i].blockName)"
                class="content__block"
                :is="resolveComponent(modelValue[i].blockName)"
                :class="{ 'content__block--nospacing': modelValue[i].noSpacing }"
                v-model="modelValue[i]"
            />
            <div class="container" v-else>
                <br />
                {{ modelValue[i].blockName }}
                <br />
                <br />
                <pre v-for="[key, value] in Object.entries(modelValue[i])">
                    <p v-if="key != 'id' && key != 'blockName'">{{ key }}: {{ value }},</p>
                </pre>
            </div>
        </template>
    </div>
</template>

<style lang="scss" scoped>
    .content {
        &__block {
            margin-bottom: clampFluid(80);
            &--nospacing {
                margin-bottom: 0;
            }
        }
    }
</style>
