package com.example.backend.Repository;

import com.example.backend.Model.Entity.Server;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;

public interface ServerRepo extends JpaRepository<Server, Integer>, JpaSpecificationExecutor<Server> {
}
