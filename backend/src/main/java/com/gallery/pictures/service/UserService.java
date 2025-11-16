package com.gallery.pictures.service;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

import org.springframework.stereotype.Service;

import com.gallery.pictures.repository.User;
import com.gallery.pictures.repository.UserRepository;

import jakarta.persistence.EntityNotFoundException;

@Service
public class UserService {

    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public List<User> getAll() {
        return this.userRepository.findAll();
    }

    public User getCurrent(Long id) {
        return this.userRepository
            .findById(id)
            .orElseThrow(() -> new EntityNotFoundException("Пользователя с id: " + id + " нет"));
    }

    public List<User> getOthers(Long id) {
        return this.userRepository
            .findAll()
            .stream()
            .filter(user -> !user.getId().equals(id))
            .collect(Collectors.toList());
    }

    public User create(User user) {
        return userRepository.save(user);
    }

    public Optional<User> authorize(String name, String password) {
        try {
            return userRepository.authorize(name, password);
            
        } catch (Exception e) {
            throw new IllegalStateException(e);
        }
    }
}
