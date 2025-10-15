export {}

declare global {
    type TBookStatus = 'published' | 'draft' | 'deleted'

    interface IBookType {
        id: number
        title: string
    }

    interface IBook {
        id: number
        title: string
        shortDescription: string | null
        image: string
        isNew: boolean
        onWishlist: boolean
        file: string | null
    }

    interface IBookDetail extends IBook {
        description: string | null
        file: string | null
        type: IBookType
        status: TBookStatus
        similar: IBook[]
        publishedAt: string
    }
}