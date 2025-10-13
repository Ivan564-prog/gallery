export {}

declare global {
    interface IUser {
        id: number
        email: string
        role: 'chief' | 'admin' | 'root' | 'missionary'
    }
}
