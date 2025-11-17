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
        onWishlist: boolean
        file: string | null
        status: TBookStatus
    }

    interface IBookDetail extends IBook {
        description: string | null
        publishedAt: string
    }

    interface ICreateBook {
        title: string
        shortDescription: string
        description: string | null
        image: File[]
    }

    interface ICreateBookErrors {
        title?: string[]
        file?: string[]
        image?: string[]
        type?: string[]
    }
}
