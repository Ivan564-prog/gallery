<script lang="ts" setup></script>

<template>
    <header class="header">
        <div class="header__top">Header-top hider</div>
        <div class="header__bottom">Header-bottom follower</div>
    </header>
</template>

<style lang="scss" scoped>
    .header {
        border: 1px solid #000;
        height: 120px;
        position: sticky;
        top: -36px;
        background-color: #fff;
        z-index: 10;
        &__top {
            height: 30%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        &__bottom {
            height: 70%;
            border-top: 1px solid #000;
            display: flex;
            align-items: center;
            justify-content: center;
        }
    }
    .logo {
        color: #6abd13;
        width: fit-content;
        rotate: -30deg;
        translate: -110px 40px;
        padding: 5px 20px;
        margin-bottom: 30px;
        font-family: Great Vibes;
        position: absolute;
        top: 30%;
        left: 100px;
        font-size: 34px;
        font-weight: 600;
    }
</style>
