<script lang="ts" setup>
    const TOASTR_NAME = 'success'
    const toastrStore = useToastrStore()
    const opened = computed({
        set: (value: boolean) => (toastrStore.activeToastr = value ? TOASTR_NAME : null),
        get: () => toastrStore.activeToastr == TOASTR_NAME,
    })
</script>

<template>
    <Toastr v-model="opened">
        <div class="toastr-success">
            <p class="toastr-success__text p3">
                {{ toastrStore.toastrMessage }}
            </p>
        </div>
    </Toastr>
</template>

<style lang="scss" scoped>
    .toastr-success {
        display: flex;
        align-items: center;
        gap: clampFluid(15);
        &__icon {
            width: 20px;
            height: 20px;
        }
    }
</style>
