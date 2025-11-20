package com.gallery.pictures.service;

import com.gallery.pictures.repository.AuthResponse;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

import org.springframework.stereotype.Service;

import com.gallery.pictures.repository.User;
import com.gallery.pictures.repository.UserRepository;
import com.gallery.pictures.repository.UserUpdateRequest;

import jakarta.persistence.EntityNotFoundException;
import jakarta.transaction.Transactional;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

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

    public User create(User user) {
        return userRepository.save(user);
    }

    public ResponseEntity<User> authorize(AuthResponse authResponse) {
        Optional<User> userOptional = userRepository.authorize(authResponse.getName(), authResponse.getPassword());

        if (userOptional.isPresent())
            return ResponseEntity.ok(userOptional.get());
        else {
            return ResponseEntity
                .status(HttpStatus.UNAUTHORIZED)
                .body(null);
        }
    }

    @Transactional
    public ResponseEntity<User> update(Long id, UserUpdateRequest userUpdateRequest) {
        Optional<User> optionalUser = userRepository.findById(id);
        if (optionalUser.isEmpty())
            return ResponseEntity.notFound().build();
        User user = optionalUser.get();

        if (userUpdateRequest.getName() != null && !userUpdateRequest.getName().isEmpty()) {
            user.setName(userUpdateRequest.getName());
        }
        if (userUpdateRequest.getPassword() != null && !userUpdateRequest.getPassword().isEmpty()) {
            user.setPassword(userUpdateRequest.getPassword());
        }
        User updatedUser = userRepository.save(user);
        return ResponseEntity.ok(updatedUser);

    }
}
