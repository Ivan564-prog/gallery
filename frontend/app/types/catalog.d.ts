export {}

declare global {
    interface ICategory {
        id: number
        title: string
        link: string
        slug: string
        image: string
        children: ICategory[]
    }

    interface ICategoryDetail extends ISeo, Omit<ICategory, children> {
        description: string | null
        content: IBaseBlock[] | null
        breadcrumbs: IBreadcrumb[]
    }

    interface IProduct {
        id: number
        title: string
        link: string
        image: string
        price: number
        priceOld: number
        quantity: number
        slug: string
    }

    interface IProductDetail extends IProduct, ISeo {
        breadcrumbs: IBreadcrumb[]
        description: string
        gallery: string[]
    }
}
