package com.jwtstegoserver.controller;

import org.springframework.stereotype.Service;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;


@Service
public class ImageService {

    @Autowired
    @Qualifier("ImageDao")
    private ImageDao imageDao;

    public void addImage(Integer id, ImageCall imageCall) {
        this.imageDao.addImage(id, imageCall);
    }

    public ImageCall getImageById(Integer id)
    {
        return this.imageDao.getImageById(id);
    }

    public int getImageCount() {
        return this.imageDao.getImageCount();
    }
}
