<script lang="ts" setup>
    const modelValue = defineModel<IFileBlock>({ required: true })
</script>

<template>
    <section class="files">
        <div class="files__container container">
            <h3 v-if="modelValue.title" class="files__title h3">{{ modelValue.title }}</h3>
            <div class="files__list">
                <a
                    v-for="file in modelValue.items"
                    :key="file.file"
                    :href="file.file"
                    class="files__item file-item"
                    target="_blank"
                >
                    <NuxtIcon class="file-item__icon" name="file" />
                    <div class="file-item__content">
                        <p class="file-item__title p1">{{ file.filename }}</p>
                        <p class="file-item__info p3">{{ file.size }}</p>
                    </div>
                </a>
            </div>
        </div>
    </section>
</template>

<style lang="scss" scoped>
    .files {
        &__title {
            margin-bottom: clampFluid(16);
        }
        &__list {
            display: flex;
            flex-direction: column;
            gap: clampFluid(32);
        }
    }

    .file-item {
        $this: &;
        display: flex;
        align-items: flex-start;
        gap: clampFluid(16);
        @include hover {
            #{$this}__title {
                color: var(--color);
            }
        }
        &__icon {
            flex: 0 0 auto;
            width: clampFluid(36);
            height: auto;
            aspect-ratio: 1;
            color: var(--color);
        }
        &__title {
            transition: .3s;
        }
        &__info {
            color: var(--black50);
            margin-top: clampFluid(8);
        }
    }
</style>
