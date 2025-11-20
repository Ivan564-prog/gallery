<script lang="ts" setup>
    const params = reactive({
        query: ''
    })

    const { data: bookList, refresh } = await useRequest<IBook[]>(
        '/api/v1/picture/',
        'GET',
        params,
    )

    const addNewBook = (book: IBook) => {
        bookList.value = [book, ...bookList.value]
    }

    const removeBook = (book: IBook) => {
        bookList.value = bookList.value.filter(item => item.id !== book.id)
    }

    const editBook = (book: IBook) => {
        bookList.value = bookList.value.map(item => {
            if (item.id === book.id) 
                return {
                    ...book,
                }
            return item
        })
    }

    const toggleWishlist = (bookId: number, status: boolean) => {
        bookList.value = bookList.value.map(book => {
            return book.id === bookId
                ? {
                      ...book,
                      onWishlist: status,
                  }
                : book
        })
    }

    watch(() => params.query, async () => {
        await refresh()
    })
</script>

<template>
    <section class="library">
        <LibraryHead class="library__head" v-model="params.query" />
        <LibraryList
            v-if="bookList?.length"
            :book-list="bookList"
        />
        <UIEmptyBanner v-else />
        <Teleport to="body">
            <LibraryDetail @toggle-wishlist="toggleWishlist" />
            <LibraryBookCreator @add-new-book="addNewBook" />
            <LibraryBookEditor 
                @edit-book="editBook"
                @remove-book="removeBook" 
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
