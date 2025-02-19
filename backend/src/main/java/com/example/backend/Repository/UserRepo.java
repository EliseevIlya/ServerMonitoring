package com.example.backend.Repository;

import com.example.backend.Model.Entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;

public interface UserRepo extends JpaRepository <User, Integer>, JpaSpecificationExecutor<User> {
}
