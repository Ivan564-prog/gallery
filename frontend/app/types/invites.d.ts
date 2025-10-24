export {}

declare global {
    interface IDioceseExtend {
        id: number
        title: string
        admin: IDioceseAdmin | null
        invite: IDioceseInvite | null
    }

    interface IDioceseAdmin {
        id: number
        image: string | null
        email: string
    }

    interface IDioceseInvite {
        id: number
        email: string
    }

    interface IInviteResponse {
        status: 'created' | 'updated'
        message: string
        invite?: IDioceseInvite
        user?: IUser
    }
}
