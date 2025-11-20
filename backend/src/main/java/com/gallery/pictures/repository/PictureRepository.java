package com.gallery.pictures.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface PictureRepository extends JpaRepository<Picture, Long> {
    List<Picture> findByTitleContainingIgnoreCase(String title);
}
