<script lang="ts" setup>
    const {
        content,
    } = defineProps<{
        content: IBook
    }>()
    const toastrStore = useToastrStore()
    const modalStore = useModalStore()
    const emits = defineEmits<{
        (event: 'open-modal', id: number): void
    }>()
    const inWishlist = ref<boolean>(content.onWishlist)

    const toggleWishlist = async () => {
        try {
            inWishlist.value = await request<boolean>('/api/v1/wishlist/book/', 'POST', {
                bookId: content.id,
            })
        } catch {
            toastrStore.showError("Ошибка добавление в избранное")
        }
    }

    const openWindow = (modalName: string) => {
        modalStore.optionalData = {
            bookId: content.id,
        }
        modalStore.openedModal = modalName
    }
</script>

<template>
    <div class="library-card">
        <button 
            class="library-card__link" 
            @click="openWindow('book-detail')"
        />
        <p v-if="content.status === 'draft'" class="library-card__banner library-card__banner--draft p3">черновик</p>
        <p v-else-if="content.isNew" class="library-card__banner library-card__banner--new p3">новинка</p>
        <div class="library-card__panel">
            <button 
                v-if="content.status === 'draft'"
                class="library-card__button" 
                @click="openWindow('book-editor')"
            >
                <NuxtIcon 
                    class="library-card__button-icon" 
                    name="pencil" 
                />
            </button>
            <button class="library-card__button" @click="toggleWishlist">
                <NuxtIcon 
                    class="library-card__button-icon" 
                    :name="inWishlist ? 'favorite-2' : 'favorite'" 
                    :class="{
                        'library-card__button-icon--active': inWishlist,
                    }"
                />
            </button>
            <a 
                download
                class="library-card__button" 
                :href="content.file || ''"
            >
                <NuxtIcon class="library-card__button-icon" name="download" />
            </a>
        </div>
        <UIImage 
            class="library-card__image"
            :src="content.image" 
            :alt="content.title"
        />
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
            background-color: var(--white);
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
            opacity: .6;
        }
    }
</style>