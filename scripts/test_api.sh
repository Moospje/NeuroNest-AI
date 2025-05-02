#!/bin/bash

# Exit on error
set -e

# Change to project root directory
cd "$(dirname "$0")/.."

# Define API URL
API_URL="http://localhost:8000"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Testing NeuroNest-AI API endpoints...${NC}"
echo "API URL: $API_URL"
echo "--------------------------------------"

# Test health check endpoint
echo -e "${YELLOW}Testing health check endpoint...${NC}"
HEALTH_RESPONSE=$(curl -s "${API_URL}/health")
echo "Response: $HEALTH_RESPONSE"
echo "--------------------------------------"

# Test user registration
echo -e "${YELLOW}Testing user registration...${NC}"
REGISTER_RESPONSE=$(curl -s -X POST "${API_URL}/api/v1/users/" \
    -H "Content-Type: application/json" \
    -d '{
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }')
echo "Response: $REGISTER_RESPONSE"
echo "--------------------------------------"

# Test login
echo -e "${YELLOW}Testing login...${NC}"
LOGIN_RESPONSE=$(curl -s -X POST "${API_URL}/api/v1/auth/login" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=testuser&password=testpassword&device_id=test-device")
echo "Response: $LOGIN_RESPONSE"

# Extract access token from login response
ACCESS_TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*' | sed 's/"access_token":"//')
REFRESH_TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"refresh_token":"[^"]*' | sed 's/"refresh_token":"//')

if [ -z "$ACCESS_TOKEN" ]; then
    echo -e "${RED}Failed to get access token${NC}"
else
    echo -e "${GREEN}Successfully obtained access token${NC}"

    # Test getting current user
    echo -e "${YELLOW}Testing get current user...${NC}"
    USER_RESPONSE=$(curl -s -X GET "${API_URL}/api/v1/users/me" \
        -H "Authorization: Bearer $ACCESS_TOKEN")
    echo "Response: $USER_RESPONSE"
    echo "--------------------------------------"

    # Test refresh token
    echo -e "${YELLOW}Testing refresh token...${NC}"
    REFRESH_RESPONSE=$(curl -s -X POST "${API_URL}/api/v1/auth/refresh" \
        -H "Content-Type: application/json" \
        -d "{
            \"refresh_token\": \"$REFRESH_TOKEN\",
            \"device_id\": \"test-device\"
        }")
    echo "Response: $REFRESH_RESPONSE"

    # Extract new access token
    NEW_ACCESS_TOKEN=$(echo $REFRESH_RESPONSE | grep -o '"access_token":"[^"]*' | sed 's/"access_token":"//')
    if [ -z "$NEW_ACCESS_TOKEN" ]; then
        echo -e "${RED}Failed to refresh token${NC}"
    else
        echo -e "${GREEN}Successfully refreshed token${NC}"
        ACCESS_TOKEN=$NEW_ACCESS_TOKEN
    fi
    echo "--------------------------------------"

    # Test creating an agent
    echo -e "${YELLOW}Testing create agent...${NC}"
    AGENT_RESPONSE=$(curl -s -X POST "${API_URL}/api/v1/agents/" \
        -H "Authorization: Bearer $ACCESS_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
            "name": "Test Agent",
            "type": "openai",
            "description": "A test agent",
            "config": {"model": "gpt-3.5-turbo"}
        }')
    echo "Response: $AGENT_RESPONSE"

    # Extract agent ID
    AGENT_ID=$(echo $AGENT_RESPONSE | grep -o '"id":"[^"]*' | sed 's/"id":"//')
    if [ -z "$AGENT_ID" ]; then
        echo -e "${RED}Failed to create agent${NC}"
    else
        echo -e "${GREEN}Successfully created agent${NC}"
    fi
    echo "--------------------------------------"

    # Test logout
    echo -e "${YELLOW}Testing logout...${NC}"
    LOGOUT_RESPONSE=$(curl -s -X POST "${API_URL}/api/v1/auth/logout" \
        -H "Authorization: Bearer $ACCESS_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
            "device_id": "test-device"
        }')
    echo "Response: $LOGOUT_RESPONSE"
    echo "--------------------------------------"
fi

echo -e "${GREEN}API testing completed!${NC}"