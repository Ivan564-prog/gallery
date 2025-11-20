package com.gallery.pictures.service;

import com.gallery.pictures.repository.Picture;
import com.gallery.pictures.repository.PictureRepository;
import com.gallery.pictures.repository.PictureRequest;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class PictureService {
    private final PictureRepository pictureRepository;

    @Value("${app.base-url:http://localhost:8000}")
    private String baseUrl;

    public PictureService(PictureRepository pictureRepository) {
        this.pictureRepository = pictureRepository;
    }

    public List<Picture> getAllPictures(String query) {
        List<Picture> pictures;
        if (query != null && !query.trim().isEmpty()) {
            pictures = pictureRepository.findByTitleContainingIgnoreCase(query.trim());
        } else {
            pictures = pictureRepository.findAll();
        }
        return pictures.stream()
                .map(this::enrichWithFullUrl)
                .collect(Collectors.toList());
    }

    public Optional<Picture> getDetailInfo(Long id) {
        return this.pictureRepository.findById(id)
                .map(this::enrichWithFullUrl);
    }

    public Picture create(PictureRequest request) throws IOException {
        String storedImagePath = saveImage(request.getImage());

        Picture picture = new Picture();
        picture.setTitle(request.getTitle());
        picture.setShortDescription(request.getShortDescription());
        picture.setDescription(request.getDescription());
        picture.setImage(storedImagePath);

        Picture savedPicture = pictureRepository.save(picture);
        return enrichWithFullUrl(savedPicture);
    }

    public Optional<Picture> delete(Long id) {
        Optional<Picture> optionalPicture = this.pictureRepository.findById(id);
        if (optionalPicture.isPresent()) {
            this.pictureRepository.deleteById(id);
        }
        return optionalPicture;
    }

    public Optional<Picture> patch(Long id, PictureRequest request) throws IOException {
        Optional<Picture> optionalPicture = this.pictureRepository.findById(id);
        if (optionalPicture.isEmpty()) {
            return Optional.empty();
        }

        Picture picture = optionalPicture.get();

        if (request.getTitle() != null && !request.getTitle().trim().isEmpty()) {
            picture.setTitle(request.getTitle());
        }
        if (request.getShortDescription() != null) {
            picture.setShortDescription(request.getShortDescription());
        }
        if (request.getDescription() != null) {
            picture.setDescription(request.getDescription());
        }

        MultipartFile image = request.getImage();
        if (image != null && !image.isEmpty()) {
            deleteImageIfExists(picture.getImage());
            picture.setImage(saveImage(image));
        }

        Picture savedPicture = pictureRepository.save(picture);
        return Optional.of(enrichWithFullUrl(savedPicture));
    }

    private Picture enrichWithFullUrl(Picture picture) {
        if (picture.getImage() != null && picture.getImage().startsWith("/")) {
            Picture enriched = new Picture();
            enriched.setId(picture.getId());
            enriched.setTitle(picture.getTitle());
            enriched.setShortDescription(picture.getShortDescription());
            enriched.setDescription(picture.getDescription());
            enriched.setImage(baseUrl + picture.getImage());
            return enriched;
        }
        return picture;
    }

    private String saveImage(MultipartFile image) throws IOException {
        if (image == null || image.isEmpty()) {
            throw new IllegalArgumentException("Image file must not be empty");
        }

        String originalFileName = image.getOriginalFilename();
        String safeFileName = (originalFileName == null || originalFileName.isBlank())
                ? "image"
                : originalFileName;
        String fileName = System.currentTimeMillis() + "_" + safeFileName;
        Path filePath = Paths.get("uploads", fileName).toAbsolutePath();

        Files.createDirectories(filePath.getParent());
        Files.copy(image.getInputStream(), filePath, StandardCopyOption.REPLACE_EXISTING);
        return "/uploads/" + fileName;
    }

    private void deleteImageIfExists(String storedPath) {
        if (storedPath == null || storedPath.isBlank()) {
            return;
        }

        String normalizedPath = storedPath.startsWith("/") ? storedPath.substring(1) : storedPath;
        Path path = Paths.get(normalizedPath);
        if (!path.isAbsolute()) {
            path = path.toAbsolutePath();
        }

        try {
            Files.deleteIfExists(path);
        } catch (IOException ignored) {
        }
    }
}
