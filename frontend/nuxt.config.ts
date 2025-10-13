import { createSvgIconsPlugin } from 'vite-plugin-svg-icons'
import path from 'path'

export default defineNuxtConfig({
    compatibilityDate: '2025-07-15',
    devtools: { enabled: true },
    modules: [
        '@nuxt/eslint', 
        '@nuxt/image', 
        '@pinia/nuxt', 
        '@nuxtjs/seo',
        'nuxt-icons',
        'vue-yandex-maps/nuxt',
    ],
    // plugins: [{ src: '~/plugins/svg-sprite.client', mode: 'client' }],
    css: [
        '~/assets/scss/reset.scss',
        '~/assets/scss/utils.scss',
        '~/assets/scss/text.scss',
        '~/assets/scss/fonts.scss',
    ],
    vite: {
        css: {
            preprocessorOptions: {
                scss: {
                    additionalData: '@use "~/assets/scss/runtime" as *;',
                },
            },
        },
        // plugins: [
        //     createSvgIconsPlugin({
        //         iconDirs: [path.resolve(process.cwd(), 'assets/icons')],
        //         symbolId: '[name]',
        //         customDomId: 'svg-icons-dom',
        //         inject: 'body-last',
        //         svgoOptions: {
        //             plugins: [
        //                 {
        //                     name: 'removeAttrs',
        //                     params: {
        //                         attrs: ['fill', 'stroke', 'style'],
        //                     },
        //                 },
        //                 {
        //                     name: 'removeDimensions',
        //                 },
        //                 {
        //                     name: 'removeStyleElement',
        //                 },
        //             ],
        //         },
        //     }),
        // ],
    },
    yandexMaps: {
        apikey: '22fbcff0-4420-4a20-81bc-789cab1db7aa',
    },
    image: {
        domains: [<string>process.env.HOST],
        format: ['webp'],
    },
    sitemap: {
        sources: [
            'https://' + <string>process.env.HOST + '/api/v1/pages/sitemap/',
            'https://' + <string>process.env.HOST + '/api/v1/pages/static_sitemap/',
            'https://' + <string>process.env.HOST + '/api/v1/catalog/category/sitemap/',
            'https://' + <string>process.env.HOST + '/api/v1/catalog/product/sitemap/',
        ],
    },
})
