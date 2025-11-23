package com.gallery.pictures.repository;

import java.util.HashMap;
import java.util.Map;

public class ValidationErrors {
    private Map<String, String[]> errors;

    public ValidationErrors() {
        this.errors = new HashMap<>();
    }

    public ValidationErrors(Map<String, String[]> errors) {
        this.errors = errors;
    }

    public void addError(String field, String message) {
        this.errors.put(field, new String[]{message});
    }

    public Map<String, String[]> getErrors() {
        return errors;
    }

    public void setErrors(Map<String, String[]> errors) {
        this.errors = errors;
    }
}

