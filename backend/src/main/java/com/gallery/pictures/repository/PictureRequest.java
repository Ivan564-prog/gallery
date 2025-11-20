package com.gallery.pictures.repository;

import org.springframework.web.multipart.MultipartFile;

public class PictureRequest {
    private String title;
    private String shortDescription;
    private String description;
    private MultipartFile image;

    // Геттеры и сеттеры
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }

    public String getShortDescription() { return shortDescription; }
    public void setShortDescription(String shortDescription) { this.shortDescription = shortDescription; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public MultipartFile getImage() { return image; }
    public void setImage(MultipartFile image) { this.image = image; }
}
