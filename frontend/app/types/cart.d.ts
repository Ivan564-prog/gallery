export {}

declare global {
    interface IPosition {
        id: number
        quantity: number
        price: number
        total: number
        product: IProduct
    }

    interface ICart {
        positions: IPosition[]
        total: number
        count: number
    }
}
