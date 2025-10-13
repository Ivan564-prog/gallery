export {}

declare global {
    type TCoord = [number, number]

    interface IMapPoint {
        id?: number
        coords: string
        balloon?: string
    }
}
