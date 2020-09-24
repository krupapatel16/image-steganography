package com.jwtstegoserver.controller;


import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.Collection;

public class ImageCall{

    private Integer id;
    private String image;

    public ImageCall(@JsonProperty("id") Integer id,
                       @JsonProperty("image") String image
    )
    {
        this.id = id;
        this.image = image;
    }

    public ImageCall() {

    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getImage() {
        return image;
    }

    public void setImage(String image) {
        this.image = image;
    }
}
