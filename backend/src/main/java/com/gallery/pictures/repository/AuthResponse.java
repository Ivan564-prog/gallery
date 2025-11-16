package com.gallery.pictures.repository;

public class AuthResponse {
    private User user;

    public AuthResponse(User user) {
        this.user = user;
    }

    public User getUser() {
        return this.user;
    }
}
