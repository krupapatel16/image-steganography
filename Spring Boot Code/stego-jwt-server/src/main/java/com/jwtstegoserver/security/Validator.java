package com.jwtstegoserver.security;

import com.jwtstegoserver.model.User;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import org.springframework.stereotype.Component;

@Component
public class Validator {

    private String secret = "This is a very big secret";

    public User validate(String token) {

        User user = null;
        try {
            Claims body = Jwts.parser()
                    .setSigningKey(secret)
                    .parseClaimsJws(token)
                    .getBody();

            user = new User();

            user.setUserName(body.getSubject());
            user.setId(Long.parseLong((String) body.get("userId")));
            user.setRole((String) body.get("role"));
        }
        catch (Exception e) {
            System.out.println(e);
        }

        return user;
    }
}
