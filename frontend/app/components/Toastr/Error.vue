<script lang="ts" setup>
    const TOASTR_NAME = 'error'
    const toastrStore = useToastrStore()
    const opened = computed({
        set: (value: boolean) => (toastrStore.activeToastr = value ? TOASTR_NAME : null),
        get: () => toastrStore.activeToastr == TOASTR_NAME,
    })
</script>

<template>
    <Toastr v-model="opened">
        <div class="toastr-error">
            <p class="toastr-error__text p3">{{ toastrStore.toastrMessage }}</p>
        </div>
    </Toastr>
</template>

<style lang="scss" scoped>
    .toastr-error {
        display: flex;
        align-items: center;
        gap: clampFluid(15);
        &__icon {
            width: 20px;
            height: 20px;
        }
    }
</style>
