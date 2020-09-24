package com.jwtstegoserver.security;

import java.math.BigInteger;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import com.jwtstegoserver.model.User;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import org.springframework.stereotype.Component;
import java.security.NoSuchAlgorithmException;

@Component
public class Generator {


    public String generate(User user) throws NoSuchAlgorithmException {

        String hash = toHexString(getSHA(user.getUserName()));

        if(hash.equals("3fc385cecae0693e0482dc9698d4d66896e7090a5bcdbe00ce63e89abbfc80ff")) {
            Claims claims = Jwts.claims()
                    .setSubject(user.getUserName());
            claims.put("userId", String.valueOf(user.getId()));
            claims.put("role", user.getRole());


            return Jwts.builder()
                    .setClaims(claims)
                    .signWith(SignatureAlgorithm.HS512, "This is a very big secret")
                    .compact();
        }
        else{
            return "Error";
        }
    }

    public static byte[] getSHA(String input) throws NoSuchAlgorithmException
    {
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        return md.digest(input.getBytes(StandardCharsets.UTF_8));
    }

    public static String toHexString(byte[] hash)
    {
        BigInteger number = new BigInteger(1, hash);
        StringBuilder hexString = new StringBuilder(number.toString(16));

        while (hexString.length() < 32)
        {
            hexString.insert(0, '0');
        }
        return hexString.toString();
    }




}
