package com.gallery.pictures.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

public interface UserRepository extends JpaRepository<User, Long> {

    @Query("SELECT u FROM User u WHERE u.name = :name AND u.password = :password")
    Optional<User> authorize(String name, String password);

    Optional<User> findByName(String name);
}
