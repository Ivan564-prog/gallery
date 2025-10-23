export {}

declare global {
    type TRequestBody = { [key: string]: any }

    interface IPage {
        id: number
        title: string
        slug: string
        image: string | null
        content: IBlock[]
    }

    interface IBreadcrumb {
        title: string
        link?: string
    }

    interface IPaginator<T> {
        hasNext: boolean
        hasPrev: boolean
        itemCount: number
        numPages: number
        page: number
        items: T[]
    }

    interface IErrorRequest<T> {
        data: T
    }

    interface IStats {
        newNotification: number 
        newBooks: number 
        newWishlist: number 
        diariesReports: number | null
    }

    interface IDiocese {
        id: number,
        title: string,
    }
}
