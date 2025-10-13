<script lang="ts" setup>
    const route = useRoute()
    const headingSlug = route.params.heading
    const pageSlug = route.params.page

    const page = ref<IPage>()
    try {
        const { data } = await useRequest<IPage>(`/api/v1/pages/${headingSlug}/`, 'GET', {
            heading: pageSlug,
        })
        page.value = data.value
    } catch {
        const { data } = await useRequest<IPage>(`/api/v1/headings/${headingSlug}/`, 'GET')
        page.value = data.value
    }
    console.log(123)

    setSeoMeta(page.value)
</script>

<template>
    <div class="page">content page headingSlug = {{ headingSlug }} pageSlug = {{ pageSlug }}</div>
</template>

<style lang="scss" scoped></style>
