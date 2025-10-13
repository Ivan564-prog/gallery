<script lang="ts" setup>
    import { Fancybox } from '@fancyapps/ui'
    import '@fancyapps/ui/dist/fancybox/fancybox.css'

    const modelValue = defineModel<IGalleryBlock>({ required: true })

    onMounted(() => {
        Fancybox.bind('[data-fancybox]')
    })
</script>

<template>
    <div class="gallery" :style="`--count-column: ${modelValue.inLine}`">
        <div class="gallery__container container">
            <div class="gallery__list">
                <a
                    v-for="item in modelValue.items"
                    :key="item.id"
                    :href="item.image"
                    class="gallery__item gallery-item"
                    :data-fancybox="`gallery-${modelValue.id}`"
                >
                    <UIImage class="gallery-item__image" :src="item.image" />
                    <p v-if="item.text" class="gallery-item__title">
                        {{ item.text }}
                    </p>
                </a>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
    .gallery {
        &__list {
            display: grid;
            grid-template-columns: repeat(var(--count-column), 1fr);
            gap: clampFluid(20);
            @include laptop {
                grid-template-columns: repeat(3, 1fr);
            }
            @include tablet {
                gap: 15px;
                grid-template-columns: repeat(2, 1fr);
            }
            @include mobile {
                grid-template-columns: 1fr;
            }
        }
    }

    .gallery-item {
        display: grid;
        gap: 19px;
        &__image {
            width: 100%;
            height: auto;
            aspect-ratio: 16 / 9;
            border-radius: clampFluid(20);
        }
        &__title {
            color: var(--black);
            @include p1;
        }
    }
</style>
