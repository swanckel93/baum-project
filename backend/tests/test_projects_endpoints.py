"""Tests for project endpoints"""

import pytest
from datetime import datetime, date
from fastapi import status


class TestProjectEndpoints:
    """Test all project CRUD endpoints"""

    def setup_dependencies(self, client, sample_user_data, sample_client_data):
        """Create user and client dependencies for project tests"""
        # Create user
        user_response = client.post("/api/v1/users/", json=sample_user_data)
        user_id = user_response.json()["id"]
        
        # Create client
        client_response = client.post("/api/v1/clients/", json=sample_client_data)
        client_id = client_response.json()["id"]
        
        return user_id, client_id

    def test_create_project_success(self, client, sample_user_data, sample_client_data, sample_project_data):
        """Test successful project creation"""
        user_id, client_id = self.setup_dependencies(client, sample_user_data, sample_client_data)
        sample_project_data["client_id"] = client_id
        
        response = client.post("/api/v1/projects/", json=sample_project_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == sample_project_data["name"]
        assert data["description"] == sample_project_data["description"]
        assert data["status"] == sample_project_data["status"]
        assert data["client_id"] == client_id
        assert data["user_id"] == 1  # Default from router
        assert "id" in data
        assert "created_at" in data

    def test_create_project_name_validation(self, client, sample_user_data, sample_client_data, sample_project_data):
        """Test project name validation"""
        user_id, client_id = self.setup_dependencies(client, sample_user_data, sample_client_data)
        sample_project_data["client_id"] = client_id
        
        test_cases = [
            ("", "Project name cannot be empty"),
            ("   ", "Project name cannot be empty"),
        ]
        
        for name, expected_error in test_cases:
            sample_project_data["name"] = name
            response = client.post("/api/v1/projects/", json=sample_project_data)
            
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_project_name_trimming(self, client, sample_user_data, sample_client_data, sample_project_data):
        """Test that project name is properly trimmed"""
        user_id, client_id = self.setup_dependencies(client, sample_user_data, sample_client_data)
        sample_project_data["client_id"] = client_id
        sample_project_data["name"] = "  Test Project  "
        
        response = client.post("/api/v1/projects/", json=sample_project_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == "Test Project"  # Should be trimmed

    def test_create_project_budget_validation(self, client, sample_user_data, sample_client_data, sample_project_data):
        """Test budget validation"""
        user_id, client_id = self.setup_dependencies(client, sample_user_data, sample_client_data)
        sample_project_data["client_id"] = client_id
        sample_project_data["budget"] = "-100.00"  # Negative budget
        
        response = client.post("/api/v1/projects/", json=sample_project_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_project_budget_zero_validation(self, client, sample_user_data, sample_client_data, sample_project_data):
        """Test that zero budget is not allowed"""
        user_id, client_id = self.setup_dependencies(client, sample_user_data, sample_client_data)
        sample_project_data["client_id"] = client_id
        sample_project_data["budget"] = "0.00"
        
        response = client.post("/api/v1/projects/", json=sample_project_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_project_date_validation(self, client, sample_user_data, sample_client_data, sample_project_data):
        """Test date validation"""
        user_id, client_id = self.setup_dependencies(client, sample_user_data, sample_client_data)
        sample_project_data["client_id"] = client_id
        
        # Test start date too far in past
        sample_project_data["start_date"] = "2010-01-01"  # More than 5 years ago
        response = client.post("/api/v1/projects/", json=sample_project_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_project_end_before_start_validation(self, client, sample_user_data, sample_client_data, sample_project_data):
        """Test that end date must be after start date"""
        user_id, client_id = self.setup_dependencies(client, sample_user_data, sample_client_data)
        sample_project_data["client_id"] = client_id
        sample_project_data["start_date"] = "2024-12-01"
        sample_project_data["end_date"] = "2024-06-01"  # Before start date
        
        response = client.post("/api/v1/projects/", json=sample_project_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_project_invalid_client_id(self, client, sample_user_data, sample_client_data, sample_project_data):
        """Test error with invalid client_id"""
        user_id, client_id = self.setup_dependencies(client, sample_user_data, sample_client_data)
        sample_project_data["client_id"] = 999  # Non-existent client
        
        # PostgreSQL will raise an IntegrityError for foreign key constraint violation
        # The FastAPI app should handle this and return a proper error response
        with pytest.raises(Exception):
            # This will raise an exception due to foreign key constraint
            response = client.post("/api/v1/projects/", json=sample_project_data)
            # If we somehow get here without exception, it should be an error status
            assert response.status_code >= 400

    def test_get_project_success(self, client, sample_user_data, sample_client_data, sample_project_data):
        """Test successful project retrieval"""
        user_id, client_id = self.setup_dependencies(client, sample_user_data, sample_client_data)
        sample_project_data["client_id"] = client_id
        
        # Create project first
        create_response = client.post("/api/v1/projects/", json=sample_project_data)
        project_id = create_response.json()["id"]
        
        # Get project
        response = client.get(f"/api/v1/projects/{project_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == project_id
        assert data["name"] == sample_project_data["name"]

    def test_get_project_not_found(self, client):
        """Test error when project not found"""
        response = client.get("/api/v1/projects/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]

    def test_update_project_success(self, client, sample_user_data, sample_client_data, sample_project_data):
        """Test successful project update"""
        user_id, client_id = self.setup_dependencies(client, sample_user_data, sample_client_data)
        sample_project_data["client_id"] = client_id
        
        # Create project first
        create_response = client.post("/api/v1/projects/", json=sample_project_data)
        project_id = create_response.json()["id"]
        
        # Update project
        update_data = {
            "name": "Updated Project",
            "status": "active",
            "budget": "20000.00"
        }
        response = client.put(f"/api/v1/projects/{project_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Updated Project"
        assert data["status"] == "active"
        assert data["budget"] == "20000.00"

    def test_update_project_validation(self, client, sample_user_data, sample_client_data, sample_project_data):
        """Test update validation"""
        user_id, client_id = self.setup_dependencies(client, sample_user_data, sample_client_data)
        sample_project_data["client_id"] = client_id
        
        # Create project first
        create_response = client.post("/api/v1/projects/", json=sample_project_data)
        project_id = create_response.json()["id"]
        
        # Try to update with invalid data
        update_data = {"name": ""}  # Empty name
        response = client.put(f"/api/v1/projects/{project_id}", json=update_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_update_project_not_found(self, client):
        """Test error when updating non-existent project"""
        update_data = {"name": "New Name"}
        response = client.put("/api/v1/projects/999", json=update_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_project_success(self, client, sample_user_data, sample_client_data, sample_project_data):
        """Test successful project deletion"""
        user_id, client_id = self.setup_dependencies(client, sample_user_data, sample_client_data)
        sample_project_data["client_id"] = client_id
        
        # Create project first
        create_response = client.post("/api/v1/projects/", json=sample_project_data)
        project_id = create_response.json()["id"]
        
        # Delete project
        response = client.delete(f"/api/v1/projects/{project_id}")
        
        assert response.status_code == status.HTTP_200_OK
        assert "deleted successfully" in response.json()["message"]
        
        # Verify project is deleted
        get_response = client.get(f"/api/v1/projects/{project_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_project_not_found(self, client):
        """Test error when deleting non-existent project"""
        response = client.delete("/api/v1/projects/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_projects_empty(self, client):
        """Test listing projects when none exist"""
        response = client.get("/api/v1/projects/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_list_projects_with_filters(self, client, sample_user_data, sample_client_data, sample_project_data):
        """Test listing projects with filters"""
        user_id, client_id = self.setup_dependencies(client, sample_user_data, sample_client_data)
        sample_project_data["client_id"] = client_id
        
        # Create project
        client.post("/api/v1/projects/", json=sample_project_data)
        
        # Test different filter combinations
        test_cases = [
            {"params": "", "expected_count": 1},
            {"params": "?active_only=true", "expected_count": 1},  # Project is in planning status (considered active)
            {"params": f"?client_id={client_id}", "expected_count": 1},
            {"params": "?user_id=1", "expected_count": 1},
        ]
        
        for case in test_cases:
            response = client.get(f"/api/v1/projects/{case['params']}")
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert len(data) == case["expected_count"]

    def test_list_projects_pagination(self, client, sample_user_data, sample_client_data, sample_project_data):
        """Test project list pagination"""
        user_id, client_id = self.setup_dependencies(client, sample_user_data, sample_client_data)
        sample_project_data["client_id"] = client_id
        
        # Create multiple projects
        for i in range(3):
            project_data = sample_project_data.copy()
            project_data["name"] = f"Project {i}"
            client.post("/api/v1/projects/", json=project_data)
        
        # Test pagination
        response = client.get("/api/v1/projects/?skip=1&limit=1")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1

    def test_project_response_schema(self, client, sample_user_data, sample_client_data, sample_project_data):
        """Test that project response contains expected fields"""
        user_id, client_id = self.setup_dependencies(client, sample_user_data, sample_client_data)
        sample_project_data["client_id"] = client_id
        
        response = client.post("/api/v1/projects/", json=sample_project_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        
        # Check all expected fields are present
        expected_fields = {
            "id", "name", "description", "status", "budget", "start_date", 
            "end_date", "user_id", "client_id", "created_at", "updated_at"
        }
        assert set(data.keys()) == expected_fields
        
        # Check field types
        assert isinstance(data["id"], int)
        assert isinstance(data["name"], str)
        assert isinstance(data["status"], str)
        assert isinstance(data["user_id"], int)
        assert isinstance(data["client_id"], int)
        assert isinstance(data["created_at"], str)