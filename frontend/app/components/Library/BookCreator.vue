<script lang="ts" setup>
    const MODAL_NAME = 'book-creator'
    const {
        typeList,
    } = defineProps<{
        typeList: IBookType[],
    }>()
    const modalStore = useModalStore()
    const toastrStore = useToastrStore()
    const opened = computed({
        set: (value: boolean) => (modalStore.openedModal = value ? MODAL_NAME : null),
        get: () => modalStore.openedModal == MODAL_NAME,
    })
    const emits = defineEmits<{
        (event:'add-new-book', book: IBook): void
    }>()
    const modalElement = ref<HTMLElement>()

    const params = reactive<ICreateBook>({
        title: '',
        shortDescription: '',
        description: '',
        image: [],
        file: [],
        type: null,
    })
    const errorsInfo = ref<ICreateBookErrors>({})

    const formattedTypeList = computed(() => {
        let typeObject: TRequestBody = {}
        typeList.forEach(type => {
            typeObject[type.id] = type.title
        })
        return typeObject
    })

    const createBook = async (status: TBookStatus) => {
        const formData = new FormData()
        errorsInfo.value = {}
        
        formData.append('title', params.title)
        formData.append('status', status)
        if (params.image[0]) 
            formData.append('image', params.image[0])
        if (params.file[0]) 
            formData.append('file', params.file[0])
        if (params.description) 
            formData.append('description', params.description)
        if (params.shortDescription) 
            formData.append('shortDescription', params.shortDescription)
        if (params.type) 
            formData.append('type', String(params.type))
        
        try {
            const newBook = await request<IBook>('/api/v1/library/book/', 'POST', formData)
            emits('add-new-book', newBook)
            opened.value = false
            toastrStore.showSuccess('Публикация успешно создана')
        } catch(error) {
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
                    <UITitledInput 
                        class="book-creator-form__item"
                        icon="star-2"
                        text="Тип публикации"
                        :error-text="errorsInfo.type && errorsInfo.type[0]"
                    >
                        <UISelect 
                            empty
                            placeholder="Выберите"
                            :items="formattedTypeList"
                            :error-text="errorsInfo.type && errorsInfo.type[0]"
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
                            :error-text="errorsInfo.file && errorsInfo.file[0]"
                            :max-files="1"
                            v-model="params.file"
                        />
                    </UITitledInput>
                    <div class="book-creator-form__photo">
                        <UITitledInput 
                            class="book-creator-form__item"
                            icon="image"
                            text="Главное изображений"
                            :error-text="errorsInfo.image && errorsInfo.image[0]"
                        >
                        <span class="book-creator-form__description p3">(необходимо добавить 1 фото)</span>
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
                        <UITextarea placeholder="Напишите краткое описание " v-model="params.shortDescription" />
                    </UITitledInput>
                    <UITitledInput 
                        class="book-creator-form__item"
                        icon="menu"
                        text="Описание"
                        variant="flex-start"
                    >
                        <WidgetTextEditor class="book-creator-form__text-editor" v-model="params.description" />
                    </UITitledInput>
                </div>
            </form>
        </template>
        <template v-slot:footer>
            <div class="book-creator-footer">
                <UIButton 
                    class="book-creator-footer__button"
                    font-size="big"
                    @click="createBook('published')"
                >Добавить публикацию</UIButton>
                <UIButton 
                    class="book-creator-footer__button" 
                    color-variant="gray"
                    font-size="big"
                    @click="createBook('draft')"
                >Сохранить черновик</UIButton>
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