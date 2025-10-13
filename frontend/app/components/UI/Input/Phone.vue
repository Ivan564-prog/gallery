<script lang="ts" setup>
    const modelValue = defineModel<string>()
    const MASK = '+7 ### ###-##-##'
    const FIRST_SYMBOLS = ['7', '8']
    const keydown = (event: KeyboardEvent) => {
        if (['e', '+', '-'].includes(event.key) || event.key.slice(0, 5) == 'Arrow') event.preventDefault()
    }

    const inputChar = (input: HTMLInputElement, key: string, inEnd: boolean) => {
        let cursor = input.selectionStart as number
        if (inEnd) cursor = (modelValue.value as string).length

        if (FIRST_SYMBOLS.includes(key) && !modelValue.value) {
            modelValue.value = MASK.slice(0, MASK.indexOf('#'))
            return
        }

        if (isNaN(parseInt(key))) return
        const endAddedIndex = MASK.slice(cursor).indexOf('#') + cursor + 1
        const added = MASK.slice(cursor, endAddedIndex).replace('#', key)
        modelValue.value =
            (modelValue.value as string).slice(0, cursor) +
            added +
            (modelValue.value as string).slice(added.length + cursor)
    }

    const clickHandler = (event: Event) => {
        const input = <HTMLInputElement>event.target
        const maxLen = input.value.length
        input.setSelectionRange(maxLen, maxLen)
    }

    const pasteHandler = (event: ClipboardEvent) => {
        event.preventDefault()
        if (!event.clipboardData) return
        const data = event.clipboardData.getData('text')
        data.replace('+7', '7')
        for (let i = 0; i < data.length; i++) {
            inputChar(<HTMLInputElement>event.target, event.clipboardData.getData('text')[i], true)
        }
    }

    const beforeinputHandler = (event: InputEvent) => {
        event.preventDefault()
        const key = event.data
        if (key) inputChar(<HTMLInputElement>event.target, key, false)

        const cursor = (<HTMLInputElement>event.target).selectionStart as number
        if (event.inputType == 'deleteContentBackward') {
            const removeIndex = MASK.slice(0, cursor).lastIndexOf('#')
            if (removeIndex == -1) modelValue.value = ''
            else
                modelValue.value =
                    (modelValue.value as string).slice(0, removeIndex) +
                    (modelValue.value as string).slice(cursor)
        }
    }
</script>

<template>
    <UIInputBase
        v-model="modelValue"
        @keydown="keydown"
        @click="clickHandler"
        @paste="pasteHandler"
        @beforeinput="beforeinputHandler"
    />
</template>

<style lang="scss" scoped></style>
