<script lang="ts" setup>
    const bookType = ref<number | undefined>(undefined)
    const requestParams = computed(() => {
        if (bookType.value === -1)
            return {
                inWishlist: true,
            }
        else 
            return {
                bookType: bookType.value,
            }
    })
    
    const { data: bookList, refresh } = await useRequest<IBook[]>(
        '/api/v1/library/book/', 
        'GET', 
        requestParams
    )     
    const { data: typeList } = await useRequest<IBookType[]>('/api/v1/library/book_type/')

    const addNewBook = (book: IBook) => {
        bookList.value.push(book)
    }

    watch(() => requestParams.value, async () => {
        await refresh()
    })
</script>

<template>
    <section class="library">
        <LibraryHead 
            class="library__head" 
            :type-list="typeList"
            v-model="bookType" 
        />
        <LibraryList 
            v-if="bookList.length" 
            :book-list="bookList" 
        />
        <UIEmptyBanner v-else />
        <Teleport to="body">
            <LibraryDetail />
            <LibraryBookCreator 
                :type-list="typeList"
                @add-new-book="addNewBook"
            />
        </Teleport>
    </section>
</template>

<style lang="scss" scoped>
    .library {
        &__head {
            margin-bottom: clampFluid(45);
        }
    }
</style>