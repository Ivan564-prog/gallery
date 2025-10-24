<script lang="ts" setup>
    const modelValue = defineModel<number>()
    const { totalMin, maxValue, step, baseOffset } = defineProps<{
        totalMin: number
        maxValue: number
        step: number
        baseOffset: number
    }>()
    const emits = defineEmits<{
        (event: 'updateValue'): void
    }>()
    const isDragged = ref<boolean>()
    const handleElement = ref<HTMLDivElement>()

    const mouseDownHandler = (event: MouseEvent) => {
        document.body.style.cursor = 'pointer'
        document.body.style.userSelect = 'none'
        isDragged.value = true
    }

    const mouseUpHandler = () => {
        document.body.style.cursor = ''
        document.body.style.userSelect = ''
        isDragged.value = false
    }

    const mouseMoveHandler = (event: MouseEvent) => {
        if (!isDragged.value) return

        const trueOffset = event.clientX - totalMin
        const roundedOffset = trueOffset - (trueOffset % step) + Math.round((trueOffset % step) / step) * step
        let limitedOffset = 0
        if (!baseOffset) {
            limitedOffset = Math.max(baseOffset, Math.min(maxValue, roundedOffset))
        } else {
            limitedOffset = Math.max(baseOffset, Math.min(maxValue - baseOffset, roundedOffset))
        }
        modelValue.value = Math.round(limitedOffset)
        emits('updateValue')
    }

    onMounted(() => {
        document.addEventListener('mousemove', mouseMoveHandler)
        document.addEventListener('mouseup', mouseUpHandler)
    })
</script>

<template>
    <div
        class="slider-input-handle"
        @mouseup="mouseUpHandler"
        @mousedown="mouseDownHandler"
        ref="handleElement"
        :style="`left: ${modelValue}px;`"
    ></div>
</template>

<style lang="scss" scoped>
    .slider-input-handle {
        border-radius: 50%;
        width: 15px;
        height: 15px;
        background-color: #62ee46;
        cursor: pointer;
        position: absolute;
        translate: -50% 0;
    }
</style>
