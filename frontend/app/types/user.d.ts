export {}

declare global {
    interface IUser {
        id: number
        email: string
        role: 'chief' | 'admin' | 'root' | 'missionary'
        image: string | null
        surname: string | null
        patronymic: string | null
        dateOfBirth: string | null
        city: string | null
        phone: string | null
        diocese: string | null
    }
}
