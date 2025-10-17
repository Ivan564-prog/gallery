<script lang="ts" setup>
    const modelValue = defineModel<string | number>()
    const text = ref<string>('')
    const isOpened = ref<boolean>(false)
    const { 
        readonly = true, 
        items, 
        empty 
    } = defineProps<{
        items: {
            [key: string | number]: string
        }
        placeholder?: string
        readonly?: boolean
        empty?: boolean
        errorText?: string
    }>()

    const select = (key: string | number) => {
        text.value = items[key]!
        modelValue.value = key
        isOpened.value = false
    }

    if (!empty && !modelValue.value) {
        modelValue.value = Object.keys(items)[0]
        text.value = items[Object.keys(items)[0]]
    }

    const filteredItemKeys = computed(() => {
        if (!readonly && text.value.length)
            return Object.keys(items).filter(key =>
                items[key]!.toLowerCase().includes(text.value.toLowerCase()),
            )
        return Object.keys(items)
    })
</script>

<template>
    <div class="ui-select" v-click-outside="() => (isOpened = false)">
        <div class="ui-select__field" @mousedown="() => (isOpened = !isOpened)">
            <UIInput
                class="ui-select__value"
                :placeholder="placeholder"
                :readonly="readonly"
                :error-text="errorText"
                :onInput="
                    () => {
                        modelValue = undefined
                    }
                "
                v-model="text"
            />
            <NuxtIcon class="ui-select__icon" name="arrow" />
        </div>
        <div class="ui-select__list" :class="{ 'ui-select__list--active': isOpened }">
            <div class="ui-select__list-wrapper">
                <div
                    class="ui-select-item"
                    v-if="empty"
                    @click="
                        () => {
                            text = ''
                            modelValue = undefined
                        }
                    "
                >
                    <span class="ui-select-item__text p2">—</span>
                </div>
                <div 
                    v-for="itemKey in filteredItemKeys" 
                    class="ui-select-item" 
                    :class="{
                        'ui-select-item--active': itemKey === modelValue
                    }"
                    @click="select(itemKey)"
                >
                    <span
                        class="ui-select-item__text p2" 
                    >{{ items[itemKey] }}</span>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="scss">
    .ui-select {
        position: relative;
        width: 100%;
        display: flex;
        flex-direction: column;
        z-index: 1;
        user-select: none;
        &__field {
            display: flex;
            align-items: center;
            cursor: pointer;
        }
        &__value {
            pointer-events: none;
        }
        &__icon {
            position: absolute;
            top: 50%;
            right: clampFluid(20);
            width: clampFluid(16);
            height: auto;
            aspect-ratio: 16 / 9;
            color: var(--gray-02);
            translate: 0 -50%;
        }
        &__list {
            position: absolute;
            top: 100%;
            background-color: var(--white);
            padding: 0 clampFluid(20);
            display: none;
            width: 100%;
            border: 1px solid var(--gray-04);
            border-top: none;
            &--active {
                display: block;
            }
            .ps {
                max-height: 300px;
            }
        }
        &__list-wrapper {
        }
    }

    .ui-select-item {
        padding: 3px 5px;
        cursor: pointer;
        &--active {
            pointer-events: none;
            color: var(--gray-03);
        }
        &__text {
            display: block;
            min-height: 1em;
        }
    }
</style>
