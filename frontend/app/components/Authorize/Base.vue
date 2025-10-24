<script lang="ts" setup></script>

<template>
    <section class="authorize">
        <AuthorizeForm class="authorize__form" />
    </section>
</template>

<style lang="scss" scoped>
    .authorize {
        padding: 0 20px;
        &__form {
            width: 100%;
            max-width: clampFluid(600);
            margin: clampFluid(124) auto 0;
            @include tablet {
                margin: 80px auto 0;
            }
        }
    }
</style>
