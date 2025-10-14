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

    watch(() => requestParams.value, async () => {
        console.log(requestParams.value);
        await refresh()
    })
</script>

<template>
    <section class="library">
        <LibraryHead class="library__head" v-model="bookType" />
        <LibraryList v-if="bookList.length" :book-list="bookList" />
        <UIEmptyBanner v-else />
    </section>
</template>

<style lang="scss" scoped>
    .library {
        &__head {
            margin-bottom: clampFluid(45);
        }
    }
</style>