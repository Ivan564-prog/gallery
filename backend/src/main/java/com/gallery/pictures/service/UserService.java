package com.gallery.pictures.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.gallery.pictures.repository.User;

@Service
public class UserService {

    public List<User> getUserList() {
        return List.of(
            new User(1L, "Иван", "test@inbox.ru", "admin"),
            new User(2L, "Антон", "test2@inbox.ru", "client"),
            new User(3L, "Петя", "test3@inbox.ru", "client")
        );
    }
}
