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

    interface IResetPasswordErrors {
        nonFieldErrors?: string[]
    }
}
