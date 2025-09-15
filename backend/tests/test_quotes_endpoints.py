"""Tests for quote endpoints"""

import pytest
from datetime import datetime, date, timedelta
from fastapi import status


class TestQuoteEndpoints:
    """Test all quote CRUD endpoints"""

    def setup_dependencies(self, client, sample_user_data, sample_client_data, 
                          sample_craftsman_data, sample_project_data, 
                          sample_campaign_data, sample_item_data):
        """Create all dependencies for quote tests"""
        # Create user
        user_response = client.post("/api/v1/users/", json=sample_user_data)
        user_id = user_response.json()["id"]
        
        # Create client
        client_response = client.post("/api/v1/clients/", json=sample_client_data)
        client_id = client_response.json()["id"]
        
        # Create craftsman
        craftsman_response = client.post("/api/v1/craftsmen/", json=sample_craftsman_data)
        craftsman_id = craftsman_response.json()["id"]
        
        # Create project
        sample_project_data["client_id"] = client_id
        project_response = client.post("/api/v1/projects/", json=sample_project_data)
        project_id = project_response.json()["id"]
        
        # Create campaign
        sample_campaign_data["project_id"] = project_id
        campaign_response = client.post("/api/v1/campaigns/", json=sample_campaign_data)
        campaign_id = campaign_response.json()["id"]
        
        # Create item
        sample_item_data["campaign_id"] = campaign_id
        item_response = client.post("/api/v1/items/", json=sample_item_data)
        item_id = item_response.json()["id"]
        
        return user_id, client_id, craftsman_id, project_id, campaign_id, item_id

    def test_create_quote_success(self, client, sample_user_data, sample_client_data,
                                 sample_craftsman_data, sample_project_data, 
                                 sample_campaign_data, sample_item_data, sample_quote_data):
        """Test successful quote creation"""
        user_id, client_id, craftsman_id, project_id, campaign_id, item_id = self.setup_dependencies(
            client, sample_user_data, sample_client_data, sample_craftsman_data,
            sample_project_data, sample_campaign_data, sample_item_data
        )
        
        sample_quote_data["item_id"] = item_id
        sample_quote_data["craftsman_id"] = craftsman_id
        
        response = client.post("/api/v1/quotes/", json=sample_quote_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["price"] == sample_quote_data["price"]
        assert data["currency"] == sample_quote_data["currency"]
        assert data["status"] == sample_quote_data["status"]
        assert data["item_id"] == item_id
        assert data["craftsman_id"] == craftsman_id
        assert "id" in data
        assert "created_at" in data

    def test_create_quote_price_validation(self, client, sample_user_data, sample_client_data,
                                          sample_craftsman_data, sample_project_data, 
                                          sample_campaign_data, sample_item_data, sample_quote_data):
        """Test quote price validation"""
        user_id, client_id, craftsman_id, project_id, campaign_id, item_id = self.setup_dependencies(
            client, sample_user_data, sample_client_data, sample_craftsman_data,
            sample_project_data, sample_campaign_data, sample_item_data
        )
        
        sample_quote_data["item_id"] = item_id
        sample_quote_data["craftsman_id"] = craftsman_id
        
        test_cases = [
            ("0", "greater than 0"),
            ("-100.00", "greater than 0"),
            ("2000000.00", "Price cannot exceed 1,000,000"),
        ]
        
        for price, expected_error in test_cases:
            sample_quote_data["price"] = price
            response = client.post("/api/v1/quotes/", json=sample_quote_data)
            
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_quote_valid_until_validation(self, client, sample_user_data, sample_client_data,
                                                sample_craftsman_data, sample_project_data, 
                                                sample_campaign_data, sample_item_data, sample_quote_data):
        """Test quote valid_until date validation"""
        user_id, client_id, craftsman_id, project_id, campaign_id, item_id = self.setup_dependencies(
            client, sample_user_data, sample_client_data, sample_craftsman_data,
            sample_project_data, sample_campaign_data, sample_item_data
        )
        
        sample_quote_data["item_id"] = item_id
        sample_quote_data["craftsman_id"] = craftsman_id
        
        # Test date in the past
        yesterday = (datetime.now() - timedelta(days=1)).date().isoformat()
        sample_quote_data["valid_until"] = yesterday
        response = client.post("/api/v1/quotes/", json=sample_quote_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Test date too far in future (more than 1 year)
        far_future = (datetime.now() + timedelta(days=400)).date().isoformat()
        sample_quote_data["valid_until"] = far_future
        response = client.post("/api/v1/quotes/", json=sample_quote_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_quote_valid_until_success(self, client, sample_user_data, sample_client_data,
                                            sample_craftsman_data, sample_project_data, 
                                            sample_campaign_data, sample_item_data, sample_quote_data):
        """Test valid valid_until date"""
        user_id, client_id, craftsman_id, project_id, campaign_id, item_id = self.setup_dependencies(
            client, sample_user_data, sample_client_data, sample_craftsman_data,
            sample_project_data, sample_campaign_data, sample_item_data
        )
        
        sample_quote_data["item_id"] = item_id
        sample_quote_data["craftsman_id"] = craftsman_id
        
        # Test valid future date
        valid_date = (datetime.now() + timedelta(days=30)).date().isoformat()
        sample_quote_data["valid_until"] = valid_date
        
        response = client.post("/api/v1/quotes/", json=sample_quote_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["valid_until"] == valid_date

    def test_create_quote_whatsapp_message_validation(self, client, sample_user_data, sample_client_data,
                                                     sample_craftsman_data, sample_project_data, 
                                                     sample_campaign_data, sample_item_data, sample_quote_data):
        """Test WhatsApp message validation"""
        user_id, client_id, craftsman_id, project_id, campaign_id, item_id = self.setup_dependencies(
            client, sample_user_data, sample_client_data, sample_craftsman_data,
            sample_project_data, sample_campaign_data, sample_item_data
        )
        
        sample_quote_data["item_id"] = item_id
        sample_quote_data["craftsman_id"] = craftsman_id
        
        # Test message too long (over 4096 characters)
        long_message = "a" * 5000
        sample_quote_data["whatsapp_message"] = long_message
        
        response = client.post("/api/v1/quotes/", json=sample_quote_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_quote_whatsapp_message_trimming(self, client, sample_user_data, sample_client_data,
                                                   sample_craftsman_data, sample_project_data, 
                                                   sample_campaign_data, sample_item_data, sample_quote_data):
        """Test WhatsApp message trimming"""
        user_id, client_id, craftsman_id, project_id, campaign_id, item_id = self.setup_dependencies(
            client, sample_user_data, sample_client_data, sample_craftsman_data,
            sample_project_data, sample_campaign_data, sample_item_data
        )
        
        sample_quote_data["item_id"] = item_id
        sample_quote_data["craftsman_id"] = craftsman_id
        sample_quote_data["whatsapp_message"] = "  Message with spaces  "
        
        response = client.post("/api/v1/quotes/", json=sample_quote_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["whatsapp_message"] == "Message with spaces"

    def test_create_quote_margin_validation(self, client, sample_user_data, sample_client_data,
                                          sample_craftsman_data, sample_project_data, 
                                          sample_campaign_data, sample_item_data, sample_quote_data):
        """Test margin percentage validation"""
        user_id, client_id, craftsman_id, project_id, campaign_id, item_id = self.setup_dependencies(
            client, sample_user_data, sample_client_data, sample_craftsman_data,
            sample_project_data, sample_campaign_data, sample_item_data
        )
        
        sample_quote_data["item_id"] = item_id
        sample_quote_data["craftsman_id"] = craftsman_id
        
        test_cases = [
            ("-5.00", "greater than or equal to 0"),
            ("150.00", "less than or equal to 100"),
        ]
        
        for margin, expected_error in test_cases:
            sample_quote_data["margin_percentage"] = margin
            response = client.post("/api/v1/quotes/", json=sample_quote_data)
            
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_quote_success(self, client, sample_user_data, sample_client_data,
                              sample_craftsman_data, sample_project_data, 
                              sample_campaign_data, sample_item_data, sample_quote_data):
        """Test successful quote retrieval"""
        user_id, client_id, craftsman_id, project_id, campaign_id, item_id = self.setup_dependencies(
            client, sample_user_data, sample_client_data, sample_craftsman_data,
            sample_project_data, sample_campaign_data, sample_item_data
        )
        
        sample_quote_data["item_id"] = item_id
        sample_quote_data["craftsman_id"] = craftsman_id
        
        # Create quote first
        create_response = client.post("/api/v1/quotes/", json=sample_quote_data)
        quote_id = create_response.json()["id"]
        
        # Get quote
        response = client.get(f"/api/v1/quotes/{quote_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == quote_id
        assert data["price"] == sample_quote_data["price"]

    def test_get_quote_not_found(self, client):
        """Test error when quote not found"""
        response = client.get("/api/v1/quotes/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]

    def test_update_quote_success(self, client, sample_user_data, sample_client_data,
                                 sample_craftsman_data, sample_project_data, 
                                 sample_campaign_data, sample_item_data, sample_quote_data):
        """Test successful quote update"""
        user_id, client_id, craftsman_id, project_id, campaign_id, item_id = self.setup_dependencies(
            client, sample_user_data, sample_client_data, sample_craftsman_data,
            sample_project_data, sample_campaign_data, sample_item_data
        )
        
        sample_quote_data["item_id"] = item_id
        sample_quote_data["craftsman_id"] = craftsman_id
        
        # Create quote first
        create_response = client.post("/api/v1/quotes/", json=sample_quote_data)
        quote_id = create_response.json()["id"]
        
        # Update quote
        update_data = {
            "price": "200.00",
            "status": "approved",
            "margin_percentage": "25.00"
        }
        response = client.put(f"/api/v1/quotes/{quote_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["price"] == "200.00"
        assert data["status"] == "approved"
        assert data["margin_percentage"] == "25.00"

    def test_update_quote_validation(self, client, sample_user_data, sample_client_data,
                                    sample_craftsman_data, sample_project_data, 
                                    sample_campaign_data, sample_item_data, sample_quote_data):
        """Test update validation"""
        user_id, client_id, craftsman_id, project_id, campaign_id, item_id = self.setup_dependencies(
            client, sample_user_data, sample_client_data, sample_craftsman_data,
            sample_project_data, sample_campaign_data, sample_item_data
        )
        
        sample_quote_data["item_id"] = item_id
        sample_quote_data["craftsman_id"] = craftsman_id
        
        # Create quote first
        create_response = client.post("/api/v1/quotes/", json=sample_quote_data)
        quote_id = create_response.json()["id"]
        
        # Try to update with invalid data
        update_data = {"price": "-50.00"}  # Negative price
        response = client.put(f"/api/v1/quotes/{quote_id}", json=update_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_delete_quote_success(self, client, sample_user_data, sample_client_data,
                                 sample_craftsman_data, sample_project_data, 
                                 sample_campaign_data, sample_item_data, sample_quote_data):
        """Test successful quote deletion"""
        user_id, client_id, craftsman_id, project_id, campaign_id, item_id = self.setup_dependencies(
            client, sample_user_data, sample_client_data, sample_craftsman_data,
            sample_project_data, sample_campaign_data, sample_item_data
        )
        
        sample_quote_data["item_id"] = item_id
        sample_quote_data["craftsman_id"] = craftsman_id
        
        # Create quote first
        create_response = client.post("/api/v1/quotes/", json=sample_quote_data)
        quote_id = create_response.json()["id"]
        
        # Delete quote
        response = client.delete(f"/api/v1/quotes/{quote_id}")
        
        assert response.status_code == status.HTTP_200_OK
        assert "deleted successfully" in response.json()["message"]
        
        # Verify quote is deleted
        get_response = client.get(f"/api/v1/quotes/{quote_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_quotes_with_filters(self, client, sample_user_data, sample_client_data,
                                     sample_craftsman_data, sample_project_data, 
                                     sample_campaign_data, sample_item_data, sample_quote_data):
        """Test listing quotes with filters"""
        user_id, client_id, craftsman_id, project_id, campaign_id, item_id = self.setup_dependencies(
            client, sample_user_data, sample_client_data, sample_craftsman_data,
            sample_project_data, sample_campaign_data, sample_item_data
        )
        
        sample_quote_data["item_id"] = item_id
        sample_quote_data["craftsman_id"] = craftsman_id
        
        # Create quote
        client.post("/api/v1/quotes/", json=sample_quote_data)
        
        # Test different filter combinations
        test_cases = [
            {"params": "", "expected_count": 1},
            {"params": f"?item_id={item_id}", "expected_count": 1},
            {"params": f"?craftsman_id={craftsman_id}", "expected_count": 1},
            {"params": "?status_filter=pending", "expected_count": 1},
            {"params": "?pending_only=true", "expected_count": 1},
            {"params": "?approved_only=true", "expected_count": 0},
        ]
        
        for case in test_cases:
            response = client.get(f"/api/v1/quotes/{case['params']}")
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert len(data) == case["expected_count"]

    def test_quote_response_schema(self, client, sample_user_data, sample_client_data,
                                  sample_craftsman_data, sample_project_data, 
                                  sample_campaign_data, sample_item_data, sample_quote_data):
        """Test that quote response contains expected fields"""
        user_id, client_id, craftsman_id, project_id, campaign_id, item_id = self.setup_dependencies(
            client, sample_user_data, sample_client_data, sample_craftsman_data,
            sample_project_data, sample_campaign_data, sample_item_data
        )
        
        sample_quote_data["item_id"] = item_id
        sample_quote_data["craftsman_id"] = craftsman_id
        
        response = client.post("/api/v1/quotes/", json=sample_quote_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        
        # Check all expected fields are present
        expected_fields = {
            "id", "price", "currency", "description", "status", "margin_percentage",
            "valid_until", "whatsapp_message", "item_id", "craftsman_id", 
            "created_at", "updated_at"
        }
        assert set(data.keys()) == expected_fields
        
        # Check field types
        assert isinstance(data["id"], int)
        assert isinstance(data["price"], str)  # Decimal returned as string
        assert isinstance(data["currency"], str)
        assert isinstance(data["status"], str)
        assert isinstance(data["item_id"], int)
        assert isinstance(data["craftsman_id"], int)
        assert isinstance(data["created_at"], str)