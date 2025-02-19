package com.example.backend.Repository;

import com.example.backend.Model.Entity.ServerInfo;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;

public interface ServerInfoRepo extends JpaRepository<ServerInfo, Integer>, JpaSpecificationExecutor<ServerInfo> {
}
