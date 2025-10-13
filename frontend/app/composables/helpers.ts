export const setSeoMeta = (obj: ISeoObject) => {
    try {
        useSeoMeta({
            title: obj.title,
            titleTemplate: obj.metaTitle ? obj.metaTitle : undefined,
            description: obj.metaDescription
                ? obj.metaDescription
                : `${obj.title} - Информацию подробнее ищите на нашем сайте или узнавайте по телефону`,
        })
    } catch {
        console.error('Объект не подходит для сео представления')
    }
}
