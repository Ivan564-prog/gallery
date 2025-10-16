<script lang="ts" setup>
    const content = defineModel<string>({ required: true })
    const editorElement = ref<HTMLDivElement>()

    const setEditorContent = (value: string) => {
        if (!editorElement.value || !content.value) return
        editorElement.value.innerHTML = value
    }
    

    const addBold = () => {
        document.execCommand('bold', false)
    }

    const addItalic = () => {
        document.execCommand('italic', false)
    }

    const addUnderline = () => {
        document.execCommand('underline', false)
    }

    const addStrike = () => {
        document.execCommand('strikethrough', false);
    }

    const addList = () => {
        document.execCommand('insertUnorderedList', false);
    }

    const addNumericList = () => {
        document.execCommand('insertOrderedList', false);
    }

    const addLeft = () => {
        document.execCommand('styleWithCSS', false)
        document.execCommand('justifyLeft', false)
    }
    
    const addCenter = () => {
        document.execCommand('styleWithCSS', false)
        document.execCommand('justifyCenter', false)
    }

    onMounted(() => {
        setEditorContent(content.value)
    })
</script>

<template>
    <div class="text-editor">
        <div class="text-editor__panel editor-panel">
            <button 
                class="editor-panel__button" 
                type="button" 
                @click="addBold"
            >
                <NuxtIcon class="editor-panel__button-icon" name="bold" />
            </button>
            <button 
                class="editor-panel__button" 
                type="button" 
                @click="addItalic"
            >
                <NuxtIcon class="editor-panel__button-icon" name="italic" />
            </button>
            <button 
                class="editor-panel__button" 
                type="button" 
                @click="addUnderline"
            >
                <NuxtIcon class="editor-panel__button-icon" name="strike" />
            </button>
            <button 
                class="editor-panel__button" 
                type="button" 
                @click="addStrike"
            >
                <NuxtIcon class="editor-panel__button-icon" name="line" />
            </button>
            <button 
                class="editor-panel__button" 
                type="button" 
                @click="addNumericList"
            >
                <NuxtIcon class="editor-panel__button-icon" name="number-list" />
            </button>
            <button 
                class="editor-panel__button" 
                type="button" 
                @click="addList"
            >
                <NuxtIcon class="editor-panel__button-icon" name="list" />
            </button>
            <button 
                class="editor-panel__button" 
                type="button" 
                @click="addLeft"
            >
                <NuxtIcon class="editor-panel__button-icon" name="left" />
            </button>
            <button 
                class="editor-panel__button" 
                type="button" 
                @click="addCenter"
            >
                <NuxtIcon class="editor-panel__button-icon" name="center" />
            </button>
        </div>
        <div 
            contenteditable
            class="text-editor__field text-content" 
            ref="editorElement"
            @input="(event: Event) => content = (event.target as HTMLDivElement).innerHTML"
        ></div>
    </div>
</template>

<style lang="scss" scoped>
    .text-editor {
        padding: clampFluid(13) clampFluid(20);
        border: 1px solid var(--gray-04);
        &__field {
            margin-top: clampFluid(12);
        }
    }

    .editor-panel {
        display: flex;
        align-items: center;
        gap: clampFluid(11);
        width: fit-content;
        padding: clampFluid(8) clampFluid(21);
        background-color: var(--gray-06);
        border-radius: clampFluid(64);
        &__button {
            padding: clampFluid(2);
            transition: $tr;
            @include hover {
                background-color: var(--gray-04);
            }
        }
        &__button-icon {
            width: clampFluid(20);
            height: auto;
            aspect-ratio: 1;
            color: var(--gray-03);
        }
    }
</style>