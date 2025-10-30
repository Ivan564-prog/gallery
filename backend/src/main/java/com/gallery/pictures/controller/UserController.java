package com.gallery.pictures.controller;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import com.gallery.pictures.repository.User;
import com.gallery.pictures.service.UserService;

@RestController 
public class UserController {
    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping
    public List<User> testEndPoint() {
        return  this.userService.getUserList();
    }
}
