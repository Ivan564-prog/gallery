<script lang="ts" setup>
    const modelValue = defineModel<[number, number]>({ required: true })
    const { minValue, maxValue, step } = defineProps<{
        minValue: number
        maxValue: number
        step: number,
    }>()
    const handleOffset1 = ref<number>(0)
    const handleOffset2 = ref<number>(0)
    const handleMin = ref<number>(0)
    const handleMax = ref<number>(0)
    const barElement = ref<HTMLDivElement>()
    const pxStep = ref<number>(1)

    const updateValue1 = () => {
        modelValue.value[0] = Math.round((maxValue - minValue) * handleOffset1.value / barElement.value!.clientWidth + minValue)
    }
    const updateValue2 = () => {
        modelValue.value[1] = Math.round((maxValue - minValue) * handleOffset2.value / barElement.value!.clientWidth + minValue)
    }

    const setHandlesByValue = () => {
        if (barElement.value){
            handleOffset1.value = (modelValue.value[0] - minValue) / (maxValue - minValue) * barElement.value.clientWidth
            handleOffset2.value = (modelValue.value[1] - minValue) / (maxValue - minValue) * barElement.value.clientWidth
        }
    }

    watch(modelValue, setHandlesByValue, {deep: true})


    onMounted(() => {
        if (barElement.value) {
            handleMin.value = barElement.value.getBoundingClientRect().left
            handleMax.value = handleMin.value + barElement.value.clientWidth
            setHandlesByValue()
            pxStep.value = step / (maxValue - minValue) * barElement.value.clientWidth
        }
    })
</script>

<template>
    <div class="range-slider">
        <div class="range-slider__wrapper">
            <div class="range-slider__bar" ref="barElement"></div>
            <div class="range-slider__progress" :style="`left: ${handleOffset1}px ;width: ${handleOffset2 - handleOffset1}px;`"></div>
            <div class="range-slider__handles">
                <!-- totalMax для всего текущего расчета maxValue только при ограничении значения -->
                <UISliderInputHandle
                    v-model="handleOffset1"
                    :totalMin="handleMin"
                    :totalMax="handleMax"
                    :minValue="handleMin"
                    :maxValue="handleOffset2"
                    :step="pxStep"
                    :baseOffset="0"
                    @updateValue="updateValue1"
                />
                <UISliderInputHandle
                    v-model="handleOffset2"
                    :totalMin="handleMin"
                    :totalMax="handleMax"
                    :minValue="handleMin + handleOffset1"
                    :maxValue="handleMax - handleMin + handleOffset1"
                    :step="pxStep"
                    :baseOffset="handleOffset1"
                    @updateValue="updateValue2"
                />
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
    .range-slider {
        position: relative;
        height: 15px;
        padding: 0 15px;
        &__wrapper {
            position: relative;
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
        }
        &__bar {
            position: relative;
            width: 100%;
            height: 2px;
            background-color: #e4e4e4;
        }
        &__progress{
            background-color: #62ee46;
            position: absolute;
            left: 0;
            height: 2px;
            width: 10px;
        }
        &__handles {
            position: absolute;
            inset: 0;
        }
        // &__point {
        //     position: absolute;
        //     z-index: 1;
        //     top: 0;
        //     left: 0;
        //     // translate: 50% 0;
        //     width: auto;
        //     height: 100%;
        //     aspect-ratio: 1;
        //     border-radius: 50%;
        //     background-color: #000;
        //     cursor: pointer;
        // }
    }
</style>
