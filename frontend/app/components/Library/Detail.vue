<script lang="ts" setup>
    const MODAL_NAME = 'book-detail'
    const toastrStore = useToastrStore()
    const modalStore = useModalStore()
    const detailInfo = ref<IBookDetail>()
    const emits = defineEmits<{
        (event: 'toggle-wishlist', bookId: number, status: boolean): void
    }>()
    const opened = computed({
        set: (value: boolean) => (modalStore.openedModal = value ? MODAL_NAME : null),
        get: () => modalStore.openedModal == MODAL_NAME,
    })
    const inWishlist = ref<boolean | undefined>(detailInfo.value?.onWishlist)
    const formattedDate = computed(() => {
        if (!detailInfo.value?.publishedAt) return
        const date = new Date(detailInfo.value?.publishedAt)
        return `${date.getDay()} ${monthByNum(date.getMonth())} ${date.getFullYear()}`
    })

    const setDetailInfo = async () => {
        if (modalStore.optionalData.bookId)
            detailInfo.value = await request<IBookDetail>(`/api/v1/library/book/${modalStore.optionalData.bookId}/`)
    }

    const toggleWishlist = async () => {
        try {
            inWishlist.value = await request<boolean>('/api/v1/wishlist/book/', 'POST', {
                bookId: detailInfo.value!.id,
            })
            emits('toggle-wishlist', detailInfo.value!.id, inWishlist.value)
        } catch {
            toastrStore.showError("Ошибка добавление в избранное")
        }
    }

    watch(() => modalStore.optionalData.bookId, newValue => {        
        if (modalStore.optionalData.bookId)
            setDetailInfo()
    })
</script>

<template>
    <ModalBase v-model="opened">
        <template v-slot:head>
            <div class="book-detail-head">
                <div class="book-detail-head__content">
                    <h2 class="book-detail-head__title h2">{{ detailInfo?.title }}</h2>
                    <p class="book-detail-head__info p2">{{ `${formattedDate} / ${detailInfo?.type.title}` }}</p>
                </div>
                <button 
                    class="book-detail-head__button"
                    @click="toggleWishlist"
                >
                    <NuxtIcon 
                        class="book-detail-head__button-icon" 
                        :name="inWishlist ? 'favorite-2' : 'favorite'" 
                    />
                </button>
            </div>
        </template>
        <template v-slot:main>
            <div class="book-detail-main">
                <div class="book-detail-main__top">
                    <div class="book-detail-main__content">
                        <div class="book-detail-main__text text-content" v-html="detailInfo?.description"></div>
                        <UIButton 
                            download
                            class="book-detail-main__button"
                            color-variant="empty-red"
                            :to="detailInfo?.file"
                        >
                            Скачать pdf
                        </UIButton>
                        <p class="book-detail-main__text p2">Дорогие читатели, если вы хотите задать вопросы о книге или получить ее в бумажном виде — пишите нам на почту</p>
                    </div>
                    <UIImage 
                        class="book-detail-main__image" 
                        :src="detailInfo?.image"
                        :alt="detailInfo?.title"
                    />
                </div>
                <div v-if="detailInfo?.similar.length" class="book-detail-main__similar">
                    <h3 class="book-detail-main__similar-title h3">Похожие материалы:</h3>
                    <div class="book-detail-main__similar-list">
                        <LibraryCard 
                            v-for="book in detailInfo?.similar"
                            :key="book.id"
                            :content="book"
                        />
                    </div>
                </div>
            </div>
        </template>
    </ModalBase>
</template>

<style lang="scss" scoped>
    .book-detail-head {
        width: 100%;
        display: flex;
        justify-content: space-between;
        gap: clampFluid(20);
        &__content {
            display: flex;
            flex-direction: column;
            gap: clampFluid(16);
        }
        &__info {
            color: var(--gray-03);
        }
        &__button-icon {
            width: clampFluid(60);
            height: auto;
            aspect-ratio: 1;
            transition: $tr;
            @include hover {
                color: var(--color);
            }
        }
    }

    .book-detail-main {
        display: grid;
        gap: clampFluid(46);
        &__top {
            display: grid;
            grid-template-columns: 1fr clampFluid(326);
            gap: clampFluid(70);
            @include tablet {
                grid-template-columns: 1fr;
                gap: clampFluid(40);
            }
        }
        &__content {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            gap: clampFluid(30);
        }
        &__image {
            height: auto;
        }
        &__similar-list {
            margin-top: clampFluid(40);
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: clampFluid(40);
            @include tablet {
                grid-template-columns: repeat(2, 1fr);
            }
        }
    }
</style>