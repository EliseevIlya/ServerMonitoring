package com.example.backend.Model.Entity;

import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.JsonIdentityReference;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "server_info")
@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
@ToString
public class ServerInfo {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long ServerInfoID;

    @ManyToOne(cascade = CascadeType.ALL,fetch = FetchType.LAZY)
    @JoinColumn(name = "server_id")
    @JsonIdentityReference(alwaysAsId = true)
    @JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "id")
    private Server server;

    @Column(name = "platform")
    private String platform;

    @Column(name = "platform_release")
    private String platformRelease;

    @Column(name = "platform_version")
    private String platformVersion;

    @Column(name = "architecture")
    private String architecture;

    @Column(name = "hostname")
    private String hostname;

    @Column(name = "cpu_usage")
    private Double cpuUsage;

    // Для вложенных объектов используем поля типа TEXT, в которые будет сохраняться JSON
    @Column(name = "memory", columnDefinition = "TEXT")
    private String memory;

    @Column(name = "disk", columnDefinition = "TEXT")
    private String disk;

    @Column(name = "network", columnDefinition = "TEXT")
    private String network;

}
