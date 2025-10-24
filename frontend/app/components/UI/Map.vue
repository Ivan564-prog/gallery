<script lang="ts" setup>
    import type { LngLat, YMap } from '@yandex/ymaps3-types'
    import {
        YandexMap,
        YandexMapDefaultSchemeLayer,
        YandexMapDefaultFeaturesLayer,
        YandexMapDefaultMarker,
    } from 'vue-yandex-maps'

    const { points } = defineProps<{
        points: IMapPoint[]
    }>()
    const map = shallowRef<YMap | null>(null)
    const coordinates = computed(() => {
        return points.map(coord => {
            const location = coord.coords.split(',')

            const latitude = +location[0]!
            const longitude = +location[1]!

            return {
                id: coord.id,
                coords: [latitude, longitude],
            }
        })
    })
</script>

<template>
    <YandexMap
        class="ui-map"
        ref="map"
        :settings="{
            location: {
                center: (coordinates[0]?.coords as LngLat) || [55.755864, 37.617698],
                zoom: 9,
            },
        }"
    >
        <YandexMapDefaultSchemeLayer />
        <YandexMapDefaultFeaturesLayer />
        <YandexMapDefaultMarker
            v-for="coord in coordinates"
            :key="coord.id"
            :settings="{ coordinates: coord.coords as LngLat }"
        />
    </YandexMap>
</template>

<style lang="scss">
    .ui-map {
        width: 100%;
        height: 100%;
    }
</style>
