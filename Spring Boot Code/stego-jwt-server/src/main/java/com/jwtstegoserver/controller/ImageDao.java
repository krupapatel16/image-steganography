package com.jwtstegoserver.controller;

import org.springframework.stereotype.Repository;


import java.util.HashMap;
import java.util.Map;

@Repository("ImageDao")
public class ImageDao {

    private final Map<Integer, ImageCall> database;

    public ImageDao() {
        database = new HashMap<>();
    }


    public void addImage(Integer id, ImageCall imageCall) {
        database.put(id,imageCall);
    }

    public ImageCall getImageById(Integer id) {
        return database.get(id);
    }


    public int getImageCount() {
        return database.size();
    }
}
