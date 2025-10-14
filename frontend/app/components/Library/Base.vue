<script lang="ts" setup>
   const { data: bookList } = await useRequest<IBook[]>('/api/v1/library/book/')     
</script>

<template>
    <section class="library">
        <LibraryHead />
        <LibraryList class="library__list" :book-list="bookList" />
    </section>
</template>

<style lang="scss" scoped>
    .library {
        &__list {
            margin-top: clampFluid(45);
        }
    }
</style>