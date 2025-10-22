<script lang="ts" setup>
    defineProps<{
        avatar: string | null
    }>()
    const newAvatar = ref<File>()
    const toastrStore = useToastrStore()

    const isImg = (file: File) => 
        window.FileReader && file.type.includes('image')

    const getURLfromFile = (file: File) => URL.createObjectURL(file)

    const setNewAvatar = async (event: Event) => {
        const input = <HTMLInputElement>event.target
        const file = input.files && input.files[0]
        if (!file || !isImg(file)) return
        newAvatar.value = file

        const formData = new FormData()
        formData.append('image', file)

        try {
            await request(
                '/api/v1/user/',
                'PATCH',
                formData
            )
            toastrStore.showSuccess('Аватарка успешно обновлена')
        } catch {
            toastrStore.showError('Ошибка обновления аватарки')
            newAvatar.value = undefined
        }
    }
</script>

<template>
    <label class="avatar">
        <div class="avatar__wrapper">
            <UIImage 
                v-if="avatar || newAvatar" 
                class="avatar__image" 
                :src="(newAvatar && getURLfromFile(newAvatar)) || avatar" 
            />
            <div v-else class="avatar__field">
                <p class="avatar__text p3">Добавить фото</p>
            </div>
        </div>
        <p v-if="avatar || newAvatar" class="avatar__edit avatar__text p3">Изменить</p>
        <input class="avatar__input" type="file" @change="setNewAvatar">
    </label>
</template>

<style lang="scss" scoped>
    .avatar {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: clampFluid(15);
        &__wrapper {
            display: flex;
            align-items: center;
            justify-content: center;
            width: clampFluid(234);
            height: auto;
            aspect-ratio: 1;
            border-radius: 50%;
            overflow: hidden;
            background-color: var(--gray-05);
        }
        &__text {
            text-decoration: underline;
            text-decoration-skip-ink: none;
            color: var(--gray-02);
            @include hover {
                text-decoration: none;
            }
        }
        &__input {
            display: none;
        }
    }
</style>