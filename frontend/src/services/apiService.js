/**
 * API Service for FastAPI Backend
 * Handles all API requests to the FastAPI backend
 */

import api from './api';

const apiService = {
  // Auth endpoints
  auth: {
    login: async (username, password, deviceId) => {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);
      formData.append('device_id', deviceId);
      
      const response = await api.post('/api/v1/auth/login', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      // Store tokens in localStorage
      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token);
        localStorage.setItem('refresh_token', response.data.refresh_token);
        localStorage.setItem('device_id', deviceId);
      }
      
      return response.data;
    },
    
    refreshToken: async () => {
      const refreshToken = localStorage.getItem('refresh_token');
      const deviceId = localStorage.getItem('device_id');
      
      if (!refreshToken || !deviceId) {
        throw new Error('No refresh token or device ID found');
      }
      
      const response = await api.post('/api/v1/auth/refresh', {
        refresh_token: refreshToken,
        device_id: deviceId,
      });
      
      // Update tokens in localStorage
      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token);
        localStorage.setItem('refresh_token', response.data.refresh_token);
      }
      
      return response.data;
    },
    
    logout: async () => {
      const deviceId = localStorage.getItem('device_id');
      
      if (!deviceId) {
        throw new Error('No device ID found');
      }
      
      await api.post('/api/v1/auth/logout', {
        device_id: deviceId,
      });
      
      // Clear tokens from localStorage
      localStorage.removeItem('token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('device_id');
      
      return true;
    },
    
    logoutAll: async () => {
      await api.post('/api/v1/auth/logout-all');
      
      // Clear tokens from localStorage
      localStorage.removeItem('token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('device_id');
      
      return true;
    },
  },
  
  // User endpoints
  users: {
    getCurrentUser: async () => {
      const response = await api.get('/api/v1/users/me');
      return response.data;
    },
    
    updateUser: async (userData) => {
      const response = await api.put('/api/v1/users/me', userData);
      return response.data;
    },
  },
  
  // Agent endpoints
  agents: {
    getAgents: async () => {
      const response = await api.get('/api/v1/agents');
      return response.data;
    },
    
    getAgent: async (agentId) => {
      const response = await api.get(`/api/v1/agents/${agentId}`);
      return response.data;
    },
    
    createAgent: async (agentData) => {
      const response = await api.post('/api/v1/agents', agentData);
      return response.data;
    },
    
    updateAgent: async (agentId, agentData) => {
      const response = await api.put(`/api/v1/agents/${agentId}`, agentData);
      return response.data;
    },
    
    deleteAgent: async (agentId) => {
      const response = await api.delete(`/api/v1/agents/${agentId}`);
      return response.data;
    },
  },
  
  // Conversation endpoints
  conversations: {
    getConversations: async () => {
      const response = await api.get('/api/v1/conversations');
      return response.data;
    },
    
    getConversation: async (conversationId) => {
      const response = await api.get(`/api/v1/conversations/${conversationId}`);
      return response.data;
    },
    
    createConversation: async (title) => {
      const response = await api.post('/api/v1/conversations', { title });
      return response.data;
    },
    
    updateConversation: async (conversationId, conversationData) => {
      const response = await api.put(`/api/v1/conversations/${conversationId}`, conversationData);
      return response.data;
    },
    
    deleteConversation: async (conversationId) => {
      const response = await api.delete(`/api/v1/conversations/${conversationId}`);
      return response.data;
    },
    
    // Message endpoints within a conversation
    sendMessage: async (conversationId, content, agentId = null) => {
      const payload = {
        content,
      };
      
      if (agentId) {
        payload.agent_id = agentId;
      }
      
      const response = await api.post(`/api/v1/conversations/${conversationId}/messages`, payload);
      return response.data;
    },
    
    getMessages: async (conversationId) => {
      const response = await api.get(`/api/v1/conversations/${conversationId}/messages`);
      return response.data;
    },
  },
};

export default apiService;