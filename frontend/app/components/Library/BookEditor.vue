<script lang="ts" setup>
    const MODAL_NAME = 'book-editor'
    const {
        typeList,
    } = defineProps<{
        typeList: IBookType[],
    }>()
    const modalStore = useModalStore()
    const opened = computed({
        set: (value: boolean) => (modalStore.openedModal = value ? MODAL_NAME : null),
        get: () => modalStore.openedModal == MODAL_NAME,
    })
    const bookData = ref<IBookDetail>()
    const emits = defineEmits<{
        (event:'add-new-book', book: IBook): void
    }>()

    const params = reactive<ICreateBook>({
        title: '',
        shortDescription: '',
        description: '',
        image: [],
        file: [],
        type: null,
    })
    const errorsInfo = ref<ICreateBookErrors>({})

    const setBookData = async () => {
        bookData.value = await request<IBookDetail>(`/api/v1/library/book/${modalStore.optionalData.bookId}/`)
    }

    const formattedTypeList = computed(() => {
        let typeObject: TRequestBody = {}
        typeList.forEach(type => {
            typeObject[type.id] = type.title
        })
        return typeObject
    })

    const editBook = (status: TBookStatus) => {

    }

    watch(() => modalStore.optionalData.bookId, () => {
        if (modalStore.optionalData.bookId)
            setBookData()
    })
</script>

<template>
    <ModalBase v-model="opened">
        <template v-slot:head>
            <h2 class="book-creator-title h2">Редактирование публикации</h2>
        </template>
        <template v-slot:main>
            <form v-if="bookData" class="book-creator-form">
                <UIInput 
                    placeholder="Введите название заголовка" 
                    style-variant="big" 
                    v-model="bookData.title"
                />
                <div class="book-creator-form__top">
                    <UITitledInput 
                        class="book-creator-form__item"
                        icon="star-2"
                        text="Тип публикации"
                    >
                        <UISelect 
                            empty
                            placeholder="Выберите"
                            :items="formattedTypeList"
                            v-model="params.type"
                        />
                    </UITitledInput>
                    <UITitledInput 
                        class="book-creator-form__item book-creator-form__item--file"
                        icon="clip"
                        text="Прикрепить"
                    >
                        <UIFileInput 
                            description="Файл" 
                            formates="application"
                            v-model="bookData.file"
                        />
                    </UITitledInput>
                    <div class="book-creator-form__photo">
                        <UITitledInput 
                            class="book-creator-form__item"
                            icon="image"
                            text="Главное изображений"
                        >
                        <span class="book-creator-form__description p3">(необходимо добавить 1 фото)</span>
                    </UITitledInput>
                    <UIFileInput 
                        formates="image"
                        :max-files="1"
                        v-model="bookData.image"
                    />
                    </div>
                </div>
                <div class="book-creator-form__bottom">
                    <UITitledInput 
                        class="book-creator-form__item"
                        icon="menu"
                        text="Краткое описание"
                        variant="flex-start"
                    >
                        <UITextarea placeholder="Напишите краткое описание " v-model="bookData.shortDescription" />
                    </UITitledInput>
                    <UITitledInput 
                        class="book-creator-form__item"
                        icon="menu"
                        text="Описание"
                        variant="flex-start"
                    >
                        <WidgetTextEditor class="book-creator-form__text-editor" v-model="bookData.description" />
                    </UITitledInput>
                </div>
            </form>
        </template>
        <template v-slot:footer>
            <div class="book-creator-footer">
                <UIButton 
                    class="book-creator-footer__button"
                    font-size="big"
                    from="creatorBook"
                    @click="editBook('published')"
                >Добавить публикацию</UIButton>
                <UIButton 
                    class="book-creator-footer__button" 
                    color-variant="gray"
                    font-size="big"
                    from="creatorBook"
                    @click="editBook('draft')"
                >Сохранить черновик</UIButton>
                <button 
                    class="book-creator-footer__remove-button p1 p1--bold"
                    from="creatorBook"
                >Удалить</button>
            </div>
        </template>
    </ModalBase>
</template>

<style lang="scss" scoped>
    .book-creator-form {
        display: flex;
        flex-direction: column;
        gap: clampFluid(30);
        &__top,
        &__bottom {
            display: flex;
            flex-direction: column;
            gap: clampFluid(20);
            padding-top: clampFluid(30);
            border-top: 1px solid var(--gray-04);
        }
        &__top {
            gap: 0;
        }
        &__item {
            &--file {
                margin: clampFluid(16) 0 clampFluid(30);
            }
        }
        &__text-editor {
            height: clampFluid(310);
        }
        &__photo {
            display: flex;
            flex-direction: column;
            gap: clampFluid(20);
        }
        &__description {
            color: var(--gray-03);
        }
    }
    .book-creator-footer {
        display: flex;
        align-items: center;
        gap: clampFluid(10);
        &__remove-button {
            padding: 0 clampFluid(30);
            height: clampFluid(59);
            transition: $tr;
            @include hover {
                color: var(--color);
            }
        }
    }
</style>