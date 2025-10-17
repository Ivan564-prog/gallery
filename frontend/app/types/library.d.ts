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
        status: TBookStatus
    }

    interface IBookDetail extends IBook {
        description: string | null
        file: string | null
        type: IBookType
        similar: IBook[]
        publishedAt: string
    }

    interface ICreateBook {
        title: string
        shortDescription: string
        description: string | null
        image: File[]
        file: File[]
        type: number | null
    }

    interface ICreateBookErrors {
        title?: string[]
        file?: string[]
        image?: string[]
        type?: string[]
    }
}