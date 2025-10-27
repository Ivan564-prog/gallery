export {}

declare global {
    type TRole = 'chief' | 'admin' | 'root' | 'missionary'

    interface IUser {
        id: number
        email: string
        role: TRole
        image: string | null
        name: string | null
        surname: string | null
        patronymic: string | null
        dateOfBirth: string | null
        city: string | null
        phone: string | null
        diocese: IDiocese | null
        country: string | null
        region: string | null
    }

    interface IRegistrationStatus {
        success: boolean
        role: TRole
    }
}
