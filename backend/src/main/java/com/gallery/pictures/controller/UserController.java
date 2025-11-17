package com.gallery.pictures.controller;

import com.gallery.pictures.repository.AuthResponse;
import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.gallery.pictures.repository.User;
import com.gallery.pictures.repository.UserUpdateRequest;
import com.gallery.pictures.service.UserService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PatchMapping;

@RestController 
@RequestMapping(path="api/v1/user/")
public class UserController {
    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping
    public List<User> getUserList() {
        return  this.userService.getAll();
    }

    @PostMapping
    public User createUser(@RequestBody User user) {
        if (user.getName().isEmpty()) {
            throw new IllegalStateException("Имя обязательно");
        }
        return this.userService.create(user);
    }

    @GetMapping(path="/{id}/")
    public User getUser(@PathVariable Long id) {
        return this.userService.getCurrent(id);
    }

    @PostMapping(path="/authorize/")
    public ResponseEntity<User> authorizeUser(@RequestBody AuthResponse authResponse) {
        return this.userService.authorize(authResponse);
    }

    @PatchMapping(path="/{id}/")
    public ResponseEntity<User> updateUser(
        @PathVariable Long id,
        @RequestBody UserUpdateRequest userUpdateRequest
    ) {
        return this.userService.update(id, userUpdateRequest);
    }
}
