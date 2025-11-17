package com.gallery.pictures.repository;

public class AuthResponse {
    private String name;
    private String password;

    public AuthResponse() {

    }

    public AuthResponse(String name, String password) {
        this.name = name;
        this.password = password;
    }


    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return this.name;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getPassword() {
        return this.password;
    }
}
