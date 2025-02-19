package com.example.backend.Model.Entity;

import com.example.backend.Model.Enums.ServerStatus;
import jakarta.persistence.*;
import lombok.*;


@Entity
@Table(name = "server")
@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
@ToString
public class Server {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long serverID;

    @Column(name = "server_name", nullable = false)
    private String serverName;

    @Column(name = "server_type", nullable = false)
    private String serverType;

    @Column(name = "server_address",unique = true, nullable = false)
    private String serverAddress;

    @Column(name = "server_port", nullable = false)
    private String serverPort;

    @Column(name = "server_status", nullable = false)
    private ServerStatus serverStatus;

    @Column(name = "server_description", nullable = false)
    private String serverDescription;

}
