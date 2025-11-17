<script lang="ts" setup>
    const MODAL_NAME = 'book-creator'
    const modalStore = useModalStore()
    const toastrStore = useToastrStore()
    const opened = computed({
        set: (value: boolean) => (modalStore.openedModal = value ? MODAL_NAME : null),
        get: () => modalStore.openedModal == MODAL_NAME,
    })
    const emits = defineEmits<{
        (event: 'add-new-book', book: IBook): void
    }>()
    const modalElement = ref<HTMLElement>()

    const params = reactive<ICreateBook>({
        title: '',
        shortDescription: '',
        description: '',
        image: [],
    })
    const errorsInfo = ref<ICreateBookErrors>({})

    const formattedTypeList = computed(() => {
        let typeObject: TRequestBody = {}
        typeList.forEach(type => {
            typeObject[type.id] = type.title
        })
        return typeObject
    })

    const createBook = async () => {
        const formData = new FormData()
        errorsInfo.value = {}

        formData.append('title', params.title)
        if (params.image[0]) formData.append('image', params.image[0])
        if (params.description) formData.append('description', params.description)
        if (params.shortDescription) formData.append('shortDescription', params.shortDescription)

        try {
            const newBook = await request<IBook>('/api/v1/library/book/', 'POST', formData)
            emits('add-new-book', newBook)
            opened.value = false
            toastrStore.showSuccess('Публикация успешно создана')
        } catch (error) {
            errorsInfo.value = (error as IErrorRequest<ICreateBookErrors>).data
            modalElement.value?.scrollTo({
                top: 0,
                behavior: 'smooth',
            })
        }
    }
</script>

<template>
    <ModalBase ref="modalElement" v-model="opened">
        <template v-slot:head>
            <h2 class="book-creator-title h2">Новая публикация</h2>
        </template>
        <template v-slot:main>
            <form class="book-creator-form">
                <UIInput
                    placeholder="Введите название заголовка"
                    style-variant="big"
                    :error-text="errorsInfo.title && errorsInfo.title[0]"
                    v-model="params.title"
                />
                <div class="book-creator-form__top">
                    <div class="book-creator-form__photo">
                        <UITitledInput
                            class="book-creator-form__item"
                            icon="image"
                            text="Главное изображений"
                            :error-text="errorsInfo.image && errorsInfo.image[0]"
                        >
                            <span class="book-creator-form__description p3">
                                (необходимо добавить 1 фото)
                            </span>
                        </UITitledInput>
                        <UIFileInput
                            formates="image"
                            :max-files="1"
                            :error-text="errorsInfo.image && errorsInfo.image[0]"
                            v-model="params.image"
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
                        <UITextarea
                            placeholder="Напишите краткое описание "
                            v-model="params.shortDescription"
                        />
                    </UITitledInput>
                    <UITitledInput
                        class="book-creator-form__item"
                        icon="menu"
                        text="Описание"
                        variant="flex-start"
                    >
                        <WidgetTextEditor
                            class="book-creator-form__text-editor"
                            v-model="params.description"
                        />
                    </UITitledInput>
                </div>
            </form>
        </template>
        <template v-slot:footer>
            <div class="book-creator-footer">
                <UIButton
                    class="book-creator-footer__button"
                    font-size="big"
                    @click="createBook"
                >
                    Добавить публикацию
                </UIButton>
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
        @include tablet {
            align-items: normal;
            flex-direction: column;
        }
        &__button {
            @include tablet {
                width: 100%;
            }
        }
    }
</style>
