package com.jwtstegoserver.security;

import com.jwtstegoserver.model.AuthTokenUserAndPass;
import com.jwtstegoserver.model.User;
import com.jwtstegoserver.model.UserDetailsImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.authentication.dao.AbstractUserDetailsAuthenticationProvider;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.AuthorityUtils;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class AuthenticationProvider extends AbstractUserDetailsAuthenticationProvider {

    @Autowired
    private Validator validator;

    @Override
    protected void additionalAuthenticationChecks(org.springframework.security.core.userdetails.UserDetails userDetails, UsernamePasswordAuthenticationToken usernamePasswordAuthenticationToken) throws AuthenticationException {

    }

    @Override
    protected org.springframework.security.core.userdetails.UserDetails retrieveUser(String username, UsernamePasswordAuthenticationToken usernamePasswordAuthenticationToken) throws AuthenticationException {

        AuthTokenUserAndPass authTokenUserAndPass = (AuthTokenUserAndPass) usernamePasswordAuthenticationToken;
        String token = authTokenUserAndPass.getToken();

        User user = validator.validate(token);

        if (user == null) {
            throw new RuntimeException("JWT Token is incorrect");
        }

        List<GrantedAuthority> grantedAuthorities = AuthorityUtils
                .commaSeparatedStringToAuthorityList(user.getRole());
        return new UserDetailsImpl(user.getUserName(), user.getId(),
                token,
                grantedAuthorities);
    }

    @Override
    public boolean supports(Class<?> aClass) {
        return (AuthTokenUserAndPass.class.isAssignableFrom(aClass));
    }
}
