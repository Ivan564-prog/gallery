<script lang="ts" setup>
    // const { data: dioceseAccountList, status } = await useRequest<IDioceseExtend[]>('/api/v1/local_hierarchy/diocese/account/')

    const { data: dioceseAccountList, status } = useAsyncData(
        'diocese-accounts',
        () => request<IDioceseExtend[]>('/api/v1/local_hierarchy/diocese/account/')
    )
</script>

<template>
    <div class="invite-diocese">
        <template v-if="status === 'success'">
            <WidgetSearch class="invite-diocese__search" />
            <div v-if="dioceseAccountList?.length" class="invite-diocese__list">
                 <InviteDioceseItem 
                    v-for="account, index in dioceseAccountList"
                    :key="account.id"
                    v-model="dioceseAccountList[index]"
                 />   
            </div>
        </template>
        <!-- -if="status === 'pending'" -->
        <UILoader v-else class="invite-diocese__loader" />
    </div>
</template>

<style lang="scss" scoped>
    .invite-diocese {
        position: relative;
        display: flex;
        flex-direction: column;
        &__search {
            width: clampFluid(500);
        }
        &__list {
            margin-top: clampFluid(30);
        }
        &__loader {
            position: absolute;
            inset: 0;
            top: clampFluid(50);
        }
    }
</style>