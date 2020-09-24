package com.jwtstegoserver.controller;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import org.springframework.beans.factory.annotation.Autowired;

@RestController
@RequestMapping("/rest/images")
public class ImageController {

    @Autowired
    private ImageService imageService;

    @RequestMapping(method = RequestMethod.GET)
    public int getImageCount() {
        return imageService.getImageCount();
    }

    @RequestMapping(value = "/{id}", method = RequestMethod.PUT, consumes = MediaType.APPLICATION_JSON_VALUE)
    public void addImage(@PathVariable("id") Integer id, @RequestBody ImageCall imageCall) {
        imageService.addImage(id, imageCall);
    }

    @RequestMapping(value = "/{id}", method = RequestMethod.GET)
    public ImageCall getNestById(@PathVariable("id") Integer id) {
        return imageService.getImageById(id);
    }

}
