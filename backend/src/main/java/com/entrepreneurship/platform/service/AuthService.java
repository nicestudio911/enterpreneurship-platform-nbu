package com.entrepreneurship.platform.service;

import com.entrepreneurship.platform.model.entity.User;
import com.entrepreneurship.platform.repository.UserRepository;
import org.springframework.stereotype.Service;
import java.util.UUID;

@Service
public class AuthService {

    private final UserRepository userRepository;

    public AuthService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public String login(String username, String password) {
        return UUID.randomUUID().toString();
    }
}
