<script lang="ts" setup>
    const isCheckPolitic = defineModel<boolean>()
</script>

<template>
    <div class="politic-confirm">
        <UICheckbox class="politic-confirm__checkbox" v-model="isCheckPolitic" />
        <div class="politic-confirm__content">
            <span class="politic-confirm__text p3">Я соглашаюсь </span>
            <UILink class="politic-confirm__link p3" to="|politic">с Правилами обработки персональной информации</UILink>
        </div>
    </div>
</template>

<style lang="scss" scoped>
    .politic-confirm {
        display: flex;
        align-items: center;
        &__text {
            color: var(--gray-03);
        }
        &__link {
            color: var(--gray-02);
            text-decoration: underline;
            text-decoration-skip-ink: none;
            @include hover {
                text-decoration: none;
            }
        }
    }
</style>