export {}

declare global {
    type TBlock = ISeoBlock | IGalleryBlock

    interface IBaseBlock {
        id: number
        uniqueId: string
        blockName: string
    }

    interface ISeoBlock extends IBaseBlock {
        text: string
        image: string | null
    }

    interface IGalleryItem {
        id: number
        text: string | null
        image: string
    }

    interface IGalleryBlock extends IBaseBlock {
        inLine: '2' | '3' | '4'
        items: IGalleryItem[]
    }

    interface IPostItem {
        id: number
        image: string
        title: string
        description: string
        link: string
    }

    interface IHeadingBlock extends IBaseBlock {
        title: string
        heading: string
        items: IPostItem[]
    }

    interface IFileItem {
        id: number
        file: string
        filename: string
        size: string
    }

    interface IFileBlock extends IBaseBlock {
        title?: string
        items: IFileItem[]
    }
}
