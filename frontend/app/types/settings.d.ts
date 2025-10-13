export {}

declare global {
    interface ISocialContacts {
        vkLink?: string
        tgLink?: string
        waLink?: string
    }

    interface IRootSettings extends ISocialContacts {
        id: number
        address?: string
        phone?: string
        email?: string
        companyName?: string
        scripts?: string
    }

    interface IIndexSettings extends ISeoObject {
        content: IBaseBlock[] | null
    }

    interface IDomain {
        id: number
        slug: string
        name: string
    }
}
