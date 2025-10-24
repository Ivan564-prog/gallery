<script lang="ts" setup>
    defineProps<{
        bookList: IBook[]
    }>()
</script>

<template>
    <div class="book-list">
        <LibraryCard v-for="card in bookList" :key="card.id" :content="card" />
    </div>
</template>

<style lang="scss" scoped>
    .book-list {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: clampFluid(40);
        @include tablet {
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }
        @include mobile {
            grid-template-columns: repeat(2, 1fr);
        }
    }
</style>
