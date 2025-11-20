package com.entrepreneurship.platform.controller;

import com.entrepreneurship.platform.model.entity.Project;
import com.entrepreneurship.platform.service.ProjectService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/projects")
@CrossOrigin(origins = "*")
public class ProjectController {

    private final ProjectService projectService;

    public ProjectController(ProjectService projectService) {
        this.projectService = projectService;
    }

    @GetMapping
    public ResponseEntity<List<Project>> getAllProjects() {
        List<Project> projects = projectService.getAllProjects();
        return ResponseEntity.ok(projects);
    }

    @PostMapping
    public ResponseEntity<Project> createProject(@RequestBody Map<String, String> projectData) {
        String name = projectData.get("name");
        String description = projectData.get("description");
        
        Project project = new Project(name, description);
        Project savedProject = projectService.createProject(project);
        
        return ResponseEntity.ok(savedProject);
    }
}
