<script lang="ts" setup>
    const modelValue = defineModel<File[]>()
    type TFormate = 'image' | 'application'
    const { 
        totalMaxSize, 
        fileMaxSize, 
        maxFiles, 
        formates, 
        rewrite 
    } = defineProps<{
        description?: string
        totalMaxSize?: number
        fileMaxSize?: number
        maxFiles?: number
        rewrite?: boolean
        formates?: TFormate[] | TFormate
    }>()

    const fileValide = (file: File) => {
        if (fileMaxSize && file.size / 1024 / 1024 > fileMaxSize) return false
        if (formates)
            if (typeof formates === 'string' && !file.type.includes(formates)) return false
            else if (
                typeof formates !== 'string' &&
                !formates.filter(format => file.type.includes(format)).length
            )
                return false
        return true
    }

    const filesValidate = (files: File[]) => {
        if (maxFiles && maxFiles < files.length) return false
        let totalSize = 0
        files.forEach(file => {
            totalSize += file.size / 1024 / 1024
        })
        if (totalMaxSize && totalMaxSize < totalSize) return false
        return true
    }

    const inputFiles = (files: File[]) => {
        if (rewrite) modelValue.value = []
        if (filesValidate(files))
            files.forEach(file => {
                if (fileValide(file)) modelValue.value?.push(file)
            })
    }

    const removeFile = (index: number) => {
        modelValue.value?.splice(index, 1)
    }

    const getFileName = (file: File) => {
        return file.name.length > 25
            ? file.name.slice(0, 20) + '... .' + file.name.split('.')[file.name.split('.').length - 1]
            : file.name
    }

    const isImg = (file: File) => {
        return window.FileReader && file.type.includes('image')
    }

    const getURLfromFile = (file: File) => {
        return URL.createObjectURL(file)
    }

    const onInput = (event: Event) => {
        let input = <HTMLInputElement>event.target
        let files = input.files ? [...input.files] : []
        inputFiles(files)
        console.log(modelValue.value);
        
    }
</script>

<template>
    <div class="ui-file-wrapper">
        <template v-if="formates === 'image'">
            <div class="ui-file-image">
                <div v-if="modelValue?.length" class="ui-file-image__list">
                    <div 
                        v-for="file, index in modelValue"
                        class="ui-file-image__item image-item"
                    >
                        <UIImage class="image-item__picture" :src="file.webkitRelativePath" />
                        <button class="image-item__button" type="button" @click="removeFile(index)">
                            <NuxtIcon class="image-item__button-icon" name="close" />
                        </button>
                    </div>
                </div>
                <label 
                    v-if="(!maxFiles || !modelValue?.length) || ((modelValue && modelValue.length > 0) && (maxFiles < modelValue.length))" 
                    class="ui-file-image__label"
                >
                    <input multiple class="ui-file-image__input" type="file" @change="onInput" />  
                    <NuxtIcon class="ui-file-image__icon" name="plus" />
                </label>
            </div>
        </template>
        <label v-else class="ui-file-input">
            <input multiple class="drop-zone__input" type="file" @change="onInput" />
            <p v-if="description" class="ui-file-input__description p3">{{ description }}</p>
            <div class="ui-file-input__list">
                <div 
                    v-for="file, ind in modelValue"
                    class="file-item" 
                    :key="ind"
                >
                    <div class="file-item__name p3">{{ getFileName(file) }}</div>
                    <button class="file-item__remove" @click="removeFile(ind)">
                        <NuxtIcon class="file-item__remove-icon" name="close" />
                    </button>
                </div>
            </div>
        </label>
    </div>
</template>

<style lang="scss" scoped>
    .ui-file-image {
        display: flex;
        flex-wrap: wrap;
        gap: clampFluid(20);
        &__list {
            display: flex;
            flex-wrap: wrap;
            gap: clampFluid(20);
        }
        &__label {
            display: flex;
            align-items: center;
            justify-content: center;
            width: clampFluid(111);
            height: auto;
            aspect-ratio: 1;
            background-color: var(--gray-05);
            transition: $tr;
        }
        &__input {
            display: none;
        }
        &__icon {
            width: clampFluid(13);
            height: auto;
            aspect-ratio: 1;
            color: var(--black);
            transition: $tr;
        }
    }

    .image-item {
        position: relative;
        width: clampFluid(111);
        height: auto;
        aspect-ratio: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        &__button {
            position: absolute;
            top: clampFluid(7);
            right: clampFluid(7);
            width: clampFluid(10);
            height: auto;
            aspect-ratio: 1;
        }
    }

    .ui-file-input {
        &__description {
            color: var(--gray-03);
        }
        &__list {
            display: grid;
            gap: 5px;
        }
    }

    .file-item {
        display: inline-flex;
        gap: clampFluid(15);
        gap: 10px;
        align-items: center;
        &__icon {
            width: 100%;
            aspect-ratio: 1;
        }
        &__remove-icon {
            width: clampFluid(10);
            height: auto;
            aspect-ratio: 1;
            transition: $tr;
            @include hover {
                color: var(--color);
            }
        }
    }

    .drop-zone {
        border: 1px dashed #000;
        display: flex;
        height: 150px;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        &--drag-over {
            background-color: #f00;
        }
        &:hover {
            background-color: #f3f3f3;
        }
        &__input {
            display: none;
        }
    }
</style>
