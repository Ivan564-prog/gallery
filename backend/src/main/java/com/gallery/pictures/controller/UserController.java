package com.gallery.pictures.controller;

import java.util.List;
import java.util.Optional;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.gallery.pictures.repository.User;
import com.gallery.pictures.service.UserService;

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

    @GetMapping(path="/{id}/others/")
    public List<User> getOthersUsers(@PathVariable Long id) {
        return this.userService.getOthers(id);
    }

    @PostMapping(path="/authorize/")
    public Optional<User> authorizeUser(@RequestParam String name, @RequestParam String password) {
        return this.userService.authorize(name, password);
    }
}
