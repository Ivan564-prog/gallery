package com.gallery.pictures.controller;

import com.gallery.pictures.repository.Picture;
import com.gallery.pictures.repository.PictureRequest;
import com.gallery.pictures.repository.User;
import com.gallery.pictures.repository.ValidationErrors;
import com.gallery.pictures.service.PictureService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;
import java.util.Optional;

@RestController 
@RequestMapping(path="api/v1/picture/")
public class PictureController {
    private final PictureService pictureService;

    public PictureController(PictureService pictureService) {
        this.pictureService = pictureService;
    }
    
    @GetMapping
    public List<Picture> getAllPictures(@RequestParam(required = false) String query) {
        return pictureService.getAllPictures(query);
    }

    @GetMapping(path="/{id}/")
    public Optional<Picture> getDetailInfo(@PathVariable Long id) {
        return this.pictureService.getDetailInfo(id);
    }

    @PostMapping
    public ResponseEntity<?> create(
            @RequestParam("title") String title,
            @RequestParam(value = "shortDescription", required = false) String shortDescription,
            @RequestParam(value = "description", required = false) String description,
            @RequestParam("image") MultipartFile image) {
        
        try {
            ValidationErrors validationErrors = new ValidationErrors();
            boolean hasErrors = false;
            
            if (title == null || title.trim().isEmpty()) {
                validationErrors.addError("title", "Это поле обязательно для заполнения");
                hasErrors = true;
            }
            
            if (image == null || image.isEmpty()) {
                validationErrors.addError("image", "Необходимо добавить изображение");
                hasErrors = true;
            }
            
            if (hasErrors) {
                return ResponseEntity.badRequest().body(validationErrors.getErrors());
            }
            
            PictureRequest request = new PictureRequest();
            request.setTitle(title);
            request.setShortDescription(shortDescription);
            request.setDescription(description);
            request.setImage(image);
            
            Picture createdPicture = pictureService.create(request);
            
            return ResponseEntity.status(HttpStatus.CREATED).body(createdPicture);
            
        } catch (IOException e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    @DeleteMapping(path="/{id}/")
    public Optional<Picture> delete(@PathVariable Long id) {
        return this.pictureService.delete(id);
    }

    @PatchMapping(path="/{id}/")
    public ResponseEntity<Picture> patch(
            @PathVariable Long id,
            @RequestParam(value = "title", required = false) String title,
            @RequestParam(value = "shortDescription", required = false) String shortDescription,
            @RequestParam(value = "description", required = false) String description,
            @RequestParam(value = "image", required = false) MultipartFile image
    ) {
        try {
            PictureRequest request = new PictureRequest();
            request.setTitle(title);
            request.setShortDescription(shortDescription);
            request.setDescription(description);
            request.setImage(image);

            Optional<Picture> updatedPicture = pictureService.patch(id, request);

            return updatedPicture
                    .map(ResponseEntity::ok)
                    .orElseGet(() -> ResponseEntity.notFound().build());

        } catch (IOException e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

}
