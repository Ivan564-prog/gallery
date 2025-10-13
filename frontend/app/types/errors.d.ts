export {}

declare global {
    interface IHttpError<T> {
        data: T
    }
}
