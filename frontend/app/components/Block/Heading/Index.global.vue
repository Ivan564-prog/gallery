<script lang="ts" setup>
    const blockContent = defineModel<IHeadingBlock>({ required: true })
    const currentPage = ref<number>(1)
    const postList = reactive<IPostItem[]>(blockContent.value.items)
</script>

<template>
    <section class="heading">
        <div class="heading__container container">
            <h1 v-if="!blockContent?.items.length" class="heading__title h1">
                {{ blockContent?.title }}
            </h1>
            <h2 v-else class="heading__title h1">{{ blockContent?.title }}</h2>
            <BlockHeadingList v-if="postList" v-model="postList" />
            <BlockHeadingPaginationList v-else :heading="blockContent.heading" />
        </div>
    </section>
</template>

<style lang="scss" scoped>
    .heading {
    }
</style>
