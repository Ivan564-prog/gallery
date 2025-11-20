<script lang="ts" setup>
    const MODAL_NAME = 'book-detail'
    const modalStore = useModalStore()
    const detailInfo = ref<IBookDetail>()
    const opened = computed({
        set: (value: boolean) => (modalStore.openedModal = value ? MODAL_NAME : null),
        get: () => modalStore.openedModal == MODAL_NAME,
    })

    const setDetailInfo = async () => {
        if (modalStore.optionalData.bookId)
            detailInfo.value = await request<IBookDetail>(
                `/api/v1/picture/${modalStore.optionalData.bookId}/`,
            )
    }

    watch(
        () => modalStore.optionalData.bookId,
        newValue => {
            if (modalStore.optionalData.bookId) setDetailInfo()
        },
    )
</script>

<template>
    <ModalBase v-model="opened">
        <template v-slot:head>
            <div class="book-detail-head">
                <div class="book-detail-head__content">
                    <h2 class="book-detail-head__title h2">{{ detailInfo?.title }}</h2>
                </div>
            </div>
        </template>
        <template v-slot:main>
            <div class="book-detail-main">
                <div class="book-detail-main__top">
                    <div class="book-detail-main__content">
                        <div
                            class="book-detail-main__text text-content"
                            v-html="detailInfo?.description"
                        ></div>
                        <UIButton
                            class="book-detail-main__button"
                            color-variant="empty-red"
                            target="_blank"
                            :to="detailInfo?.image"
                        >
                            Скачать
                        </UIButton>
                    </div>
                    <UIImage
                        class="book-detail-main__image"
                        :src="detailInfo?.image"
                        :alt="detailInfo?.title"
                    />
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
