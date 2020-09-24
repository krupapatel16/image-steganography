package com.jwtstegoserver.controller;

import com.jwtstegoserver.security.Generator;
import com.jwtstegoserver.model.User;

import java.security.NoSuchAlgorithmException;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/token")
public class TokenController {

    private Generator generator;

    public TokenController(Generator generator) {
        this.generator = generator;
    }

    @PostMapping
    public String generate(@RequestBody final User user) throws NoSuchAlgorithmException {

        return generator.generate(user);

    }
}
