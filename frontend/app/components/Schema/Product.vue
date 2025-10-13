<script lang="ts" setup>
    const product = defineModel<IProductDetail>({ required: true })
</script>

<template>
    <div itemscope itemtype="http://schema.org/Product">
        <meta itemprop="name" :content="product.title" />
        <meta
            itemprop="description"
            :content="product.description ? product.description : 'More information on site'"
        />
        <meta itemprop="image" :content="product.image ? product.image : ''" />

        <div itemprop="offers" itemscope itemtype="http://schema.org/Offer">
            <span itemprop="price">{{ product.price }}</span>
            <span itemprop="priceCurrency">RUB</span>
        </div>
    </div>
</template>

<style lang="scss" scoped>
    div {
        display: none;
    }
</style>
