export {}

declare global {
    interface IHttpError<T> {
        data: T
    }

    interface IAuthorizeErrors {
        email?: string[]
        password?: string[]
    }

    interface IForgotPasswordErrors {
        email?: string[]
    }

    interface IPasswordErrors {
        nonFieldErrors?: string[]
    }

    interface IUserErrors {
        date?: string
        phone?: string
        password1?: string
    }
}
