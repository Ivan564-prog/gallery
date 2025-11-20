<script lang="ts" setup>
    const { content } = defineProps<{
        content: IBook
    }>()
    const toastrStore = useToastrStore()
    const modalStore = useModalStore()
    const userStore = useUserStore()
    const emits = defineEmits<{
        (event: 'open-modal', id: number): void
        (event: 'remove-book', book: IBook): void
    }>()
    const inWishlist = ref<boolean>(content.onWishlist)

    const removeBook = async () => {
        try {
            const deletedBook = await request<IBook>(`/api/v1/picture/${content.id}/`, 'DELETE')
            emits('remove-book', content)
            toastrStore.showSuccess('Публикация успешно удалена')
        } catch {
            toastrStore.showError('Ошибка удаления публикации')
        }
    }

    watch(
        () => content.onWishlist,
        newValue => {
            inWishlist.value = newValue
        },
    )

    const openWindow = (modalName: string) => {
        modalStore.optionalData = {
            bookId: content.id,
        }
        modalStore.openedModal = modalName
    }
</script>

<template>
    <div class="library-card">
        <button class="library-card__link" @click="openWindow('book-detail')"></button>
        <div class="library-card__panel">
            <a download class="library-card__button" target="_blank" :href="content.image || ''">
                <NuxtIcon class="library-card__button-icon" name="download" />
            </a>
            <button
                v-if="userStore.userData.role === 'admin'"
                class="library-card__button"
                @click="openWindow('book-editor')"
            >
                <NuxtIcon class="library-card__button-icon" name="pencil" />
            </button>
        </div>
        <UIImage class="library-card__image" :src="content.image" :alt="content.title" />
        <p class="library-card__title p2 p2--bold">{{ content.title }}</p>
        <p class="library-card__short-description p3">{{ content.shortDescription }}</p>
    </div>
</template>

<style lang="scss" scoped>
    .library-card {
        $this: &;
        position: relative;
        display: flex;
        flex-direction: column;
        &__link {
            position: absolute;
            z-index: 1;
            inset: 0;
            cursor: pointer;
            @include hover {
                & ~ #{$this}__title {
                    color: var(--color);
                }
            }
        }
        &__banner {
            position: absolute;
            top: 0;
            left: 0;
            translate: 0 -55%;
            display: inline-block;
            padding: clampFluid(2) clampFluid(10);
            color: var(--white);
            &--new {
                background-color: var(--color);
            }
            &--draft {
                background-color: var(--gray-02);
            }
        }
        &__panel {
            position: absolute;
            z-index: 2;
            top: clampFluid(15);
            right: clampFluid(15);
            display: flex;
            gap: clampFluid(10);
        }
        &__button {
            width: clampFluid(40);
            height: auto;
            aspect-ratio: 1;
            background-color: var(--white);
            @include tablet {
                width: 24px;
            }
        }
        &__button-icon {
            color: var(--black);
            transition: $tr;
            @include hover {
                color: var(--color);
            }
            &--active {
                color: var(--color);
            }
        }
        &__image {
            width: 100%;
            height: auto;
        }
        &__title {
            margin: clampFluid(10) 0 clampFluid(6);
            transition: $tr;
            @include tablet {
                margin: 6px 0 4px;
            }
        }
        &__short-description {
            opacity: 0.6;
        }
    }
</style>
