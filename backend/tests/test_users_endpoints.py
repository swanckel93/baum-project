"""Tests for user endpoints"""

from fastapi import status


class TestUserEndpoints:
    """Test all user CRUD endpoints"""

    def test_create_user_success(self, client, sample_user_data):
        """Test successful user creation"""
        response = client.post("/api/v1/users/", json=sample_user_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == sample_user_data["email"]
        assert data["full_name"] == sample_user_data["full_name"]
        assert data["phone"] == sample_user_data["phone"]
        assert data["is_active"] == sample_user_data["is_active"]
        assert data["is_admin"] == sample_user_data["is_admin"]
        assert "id" in data
        assert "created_at" in data
        assert "hashed_password" not in data  # Password should not be returned

    def test_create_user_duplicate_email(self, client, sample_user_data):
        """Test error when creating user with duplicate email"""
        # Create first user
        client.post("/api/v1/users/", json=sample_user_data)

        # Try to create another user with same email
        response = client.post("/api/v1/users/", json=sample_user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already exists" in response.json()["detail"]

    def test_create_user_invalid_email(self, client, sample_user_data):
        """Test error with invalid email format"""
        sample_user_data["email"] = "invalid-email"

        response = client.post("/api/v1/users/", json=sample_user_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_user_weak_password(self, client, sample_user_data):
        """Test error with weak password"""
        sample_user_data["password"] = "weak"

        response = client.post("/api/v1/users/", json=sample_user_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        error_detail = response.json()["detail"][0]
        assert "password" in error_detail["loc"]

    def test_create_user_password_validation(self, client, sample_user_data):
        """Test password validation rules"""
        test_cases = [
            (
                "short",
                [
                    "at least 8 characters",
                    "Password must be at least 8 characters long",
                ],
            ),
            (
                "onlylowercase",
                [
                    "uppercase letter or digit",
                    "Password must contain at least one uppercase letter or digit",
                ],
            ),
            (
                "ONLYUPPERCASE",
                [
                    "lowercase letter",
                    "Password must contain at least one lowercase letter",
                ],
            ),
        ]

        for password, expected_errors in test_cases:
            sample_user_data["password"] = password
            response = client.post("/api/v1/users/", json=sample_user_data)

            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
            error_detail = response.json()["detail"][0]
            # Check if any of the expected error messages are in the response
            assert any(err in error_detail["msg"] for err in expected_errors)

    def test_create_user_full_name_validation(self, client, sample_user_data):
        """Test full name validation"""
        test_cases = [
            ("", "Full name cannot be empty"),
            ("   ", "Full name cannot be empty"),
            ("Test@User", "Full name can only contain letters"),
            ("Test#User", "Full name can only contain letters"),
        ]

        for full_name, expected_error in test_cases:
            sample_user_data["full_name"] = full_name
            response = client.post("/api/v1/users/", json=sample_user_data)

            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_user_phone_validation(self, client, sample_user_data):
        """Test phone number validation"""
        test_cases = [
            ("123", "Phone number must be between 7 and 15 digits"),
            ("12345678901234567890", "Phone number must be between 7 and 15 digits"),
        ]

        for phone, expected_error in test_cases:
            sample_user_data["phone"] = phone
            response = client.post("/api/v1/users/", json=sample_user_data)

            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_user_name_formatting(self, client, sample_user_data):
        """Test that full name is properly formatted"""
        sample_user_data["full_name"] = "  john doe  "

        response = client.post("/api/v1/users/", json=sample_user_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["full_name"] == "John Doe"  # Should be title cased and trimmed

    def test_get_user_success(self, client, sample_user_data):
        """Test successful user retrieval"""
        # Create user first
        create_response = client.post("/api/v1/users/", json=sample_user_data)
        user_id = create_response.json()["id"]

        # Get user
        response = client.get(f"/api/v1/users/{user_id}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == user_id
        assert data["email"] == sample_user_data["email"]

    def test_get_user_not_found(self, client):
        """Test error when user not found"""
        response = client.get("/api/v1/users/999")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]

    def test_get_user_by_email_success(self, client, sample_user_data):
        """Test successful user retrieval by email"""
        # Create user first
        client.post("/api/v1/users/", json=sample_user_data)

        # Get user by email
        response = client.get(f"/api/v1/users/email/{sample_user_data['email']}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == sample_user_data["email"]

    def test_get_user_by_email_not_found(self, client):
        """Test error when user email not found"""
        response = client.get("/api/v1/users/email/nonexistent@example.com")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_user_success(self, client, sample_user_data):
        """Test successful user update"""
        # Create user first
        create_response = client.post("/api/v1/users/", json=sample_user_data)
        user_id = create_response.json()["id"]

        # Update user
        update_data = {
            "full_name": "Updated Name",
            "phone": "+9876543210",
            "is_active": False,
        }
        response = client.put(f"/api/v1/users/{user_id}", json=update_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["full_name"] == "Updated Name"
        assert data["phone"] == "+9876543210"
        assert data["is_active"] is False
        assert data["email"] == sample_user_data["email"]  # Unchanged

    def test_update_user_not_found(self, client):
        """Test error when updating non-existent user"""
        update_data = {"full_name": "New Name"}
        response = client.put("/api/v1/users/999", json=update_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_user_partial(self, client, sample_user_data):
        """Test partial user update"""
        # Create user first
        create_response = client.post("/api/v1/users/", json=sample_user_data)
        user_id = create_response.json()["id"]

        # Update only one field
        update_data = {"full_name": "Only Name Changed"}
        response = client.put(f"/api/v1/users/{user_id}", json=update_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["full_name"] == "Only Name Changed"
        assert data["email"] == sample_user_data["email"]
        assert data["phone"] == sample_user_data["phone"]

    def test_delete_user_success(self, client, sample_user_data):
        """Test successful user deletion"""
        # Create user first
        create_response = client.post("/api/v1/users/", json=sample_user_data)
        user_id = create_response.json()["id"]

        # Delete user
        response = client.delete(f"/api/v1/users/{user_id}")

        assert response.status_code == status.HTTP_200_OK
        assert "deleted successfully" in response.json()["message"]

        # Verify user is deleted
        get_response = client.get(f"/api/v1/users/{user_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_user_not_found(self, client):
        """Test error when deleting non-existent user"""
        response = client.delete("/api/v1/users/999")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_users_empty(self, client):
        """Test listing users when none exist"""
        response = client.get("/api/v1/users/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_list_users_with_data(self, client, sample_user_data):
        """Test listing users with data"""
        # Create multiple users
        created_users = []
        for i in range(3):
            user_data = sample_user_data.copy()
            user_data["email"] = f"user{i}@example.com"
            user_data["full_name"] = f"User {i}"
            response = client.post("/api/v1/users/", json=user_data)
            if response.status_code != status.HTTP_201_CREATED:
                print(f"Failed to create user {i}: {response.json()}")
            assert response.status_code == status.HTTP_201_CREATED
            created_users.append(response.json())

        response = client.get("/api/v1/users/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3

        # Verify the created users are in the response
        emails = {user["email"] for user in data}
        expected_emails = {f"user{i}@example.com" for i in range(3)}
        assert emails == expected_emails

    def test_list_users_pagination(self, client, sample_user_data):
        """Test user list pagination"""
        # Create multiple users
        for i in range(5):
            user_data = sample_user_data.copy()
            user_data["email"] = f"user{i}@example.com"
            client.post("/api/v1/users/", json=user_data)

        # Test pagination
        response = client.get("/api/v1/users/?skip=2&limit=2")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2

    def test_user_response_schema(self, client, sample_user_data):
        """Test that user response contains expected fields"""
        response = client.post("/api/v1/users/", json=sample_user_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()

        # Check all expected fields are present
        expected_fields = {
            "id",
            "email",
            "full_name",
            "phone",
            "is_active",
            "is_admin",
            "created_at",
            "updated_at",
        }
        assert set(data.keys()) == expected_fields

        # Check field types
        assert isinstance(data["id"], int)
        assert isinstance(data["email"], str)
        assert isinstance(data["full_name"], str)
        assert isinstance(data["is_active"], bool)
        assert isinstance(data["is_admin"], bool)
        assert isinstance(data["created_at"], str)

        # Password should never be in response
        assert "password" not in data
        assert "hashed_password" not in data
