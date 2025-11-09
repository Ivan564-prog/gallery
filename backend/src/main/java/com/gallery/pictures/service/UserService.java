package com.gallery.pictures.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.gallery.pictures.repository.User;
import com.gallery.pictures.repository.UserRepository;

@Service
public class UserService {

    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public List<User> getUserList() {
        return this.userRepository.findAll();
    }
}
