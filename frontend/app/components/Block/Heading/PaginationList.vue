<script lang="ts" setup>
    const { heading } = defineProps<{
        heading: string
    }>()
    const currentPage = ref<number>(1)
    const params = reactive({
        pages: currentPage.value,
    })
    const { data: paginatorPost, refresh } = await useRequest<IPaginator<IPostItem>>(
        `/api/v1/pages/${heading}/subpages`,
        'GET',
        params,
    )

    watch(currentPage, async () => {
        await refresh()
    })
</script>

<template>
    <div class="heading-wrapper">
        <div class="heading-wrapper__list">
            <CardPost v-for="post in paginatorPost.items" :key="post.id" :card-content="post" />
        </div>
        <UIPagination
            class="heading-wrapper__pagination"
            v-model:page="currentPage"
            :max-page="paginatorPost.numPages"
        />
    </div>
</template>

<style lang="scss" scoped></style>
