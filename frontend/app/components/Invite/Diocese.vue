<script lang="ts" setup>
    const query = ref<string>('')
    const { data: dioceseAccountList, status, refresh } = useAsyncData(
        'diocese-accounts',
        () => request<IDioceseExtend[]>(
                '/api/v1/local_hierarchy/diocese/account/',
                'GET',
                {
                    query: query.value,
                }
            ),
        {
            deep: true,
        },
    )

    watch(query, async () => {
        await refresh()
    })
</script>

<template>
    <div class="invite-diocese">
        <WidgetSearch class="invite-diocese__search" v-model="query" />
        <template v-if="status === 'success'">
            <div v-if="dioceseAccountList?.length" class="invite-diocese__list">
                <InviteDioceseItem
                    v-for="(account, index) in dioceseAccountList"
                    :key="account.id"
                    v-model="dioceseAccountList[index]"
                />
            </div>
        </template>
        <UILoader v-else-if="status === 'pending'" class="invite-diocese__loader" />
    </div>
</template>

<style lang="scss" scoped>
    .invite-diocese {
        position: relative;
        display: flex;
        flex-direction: column;
        &__search {
            width: clampFluid(500);
            margin-bottom: clampFluid(30);
        }
        &__loader {
            position: absolute;
            inset: 0;
            top: clampFluid(100);
        }
    }
</style>
