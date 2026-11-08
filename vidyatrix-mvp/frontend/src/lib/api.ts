const AUTH_API = 'http://localhost:8001'
const VIDEO_API = 'http://localhost:8002'
const CHAT_API = 'http://localhost:8003'

export interface User {
  id: string
  email: string
  name: string
  created_at: string
}

export interface Video {
  id: string
  user_id: string
  title: string
  filename: string
  duration: number | null
  status: 'pending' | 'processing' | 'completed' | 'failed'
  error_message: string | null
  created_at: string
}

export interface SourceCitation {
  video_id: string
  video_title: string
  start_time: number
  end_time: number
  text: string
}

export interface ChatMessage {
  id: string
  conversation_id: string
  role: 'user' | 'assistant'
  content: string
  sources: SourceCitation[]
  created_at: string
}

export interface Conversation {
  id: string
  user_id: string
  title: string
  created_at: string
}

export const authApi = {
  register: async (email: string, password: string, name: string) => {
    const response = await fetch(`${AUTH_API}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, name }),
    })
    if (!response.ok) throw new Error('Registration failed')
    return response.json()
  },

  login: async (email: string, password: string) => {
    const response = await fetch(`${AUTH_API}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    })
    if (!response.ok) throw new Error('Login failed')
    return response.json()
  },

  getMe: async (token: string) => {
    const response = await fetch(`${AUTH_API}/auth/me?token=${token}`)
    if (!response.ok) throw new Error('Failed to get user')
    return response.json()
  },
}

export const videoApi = {
  upload: async (file: File, title: string, token: string) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('title', title)
    formData.append('token', token)

    const response = await fetch(`${VIDEO_API}/api/videos/upload`, {
      method: 'POST',
      body: formData,
    })
    if (!response.ok) throw new Error('Upload failed')
    return response.json()
  },

  list: async (token: string): Promise<Video[]> => {
    const response = await fetch(`${VIDEO_API}/api/videos?token=${token}`)
    if (!response.ok) throw new Error('Failed to list videos')
    return response.json()
  },

  delete: async (videoId: string, token: string) => {
    const response = await fetch(`${VIDEO_API}/api/videos/${videoId}?token=${token}`, {
      method: 'DELETE',
    })
    if (!response.ok) throw new Error('Failed to delete video')
  },
}

export const chatApi = {
  send: async (message: string, _token: string, videoId?: string, conversationId?: string): Promise<ChatMessage> => {
    const response = await fetch(`${CHAT_API}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message,
        video_id: videoId,
        conversation_id: conversationId,
      }),
    })
    if (!response.ok) throw new Error('Failed to send message')
    return response.json()
  },

  listConversations: async (token: string): Promise<Conversation[]> => {
    const response = await fetch(`${CHAT_API}/api/chat/conversations?token=${token}`)
    if (!response.ok) throw new Error('Failed to list conversations')
    return response.json()
  },

  getMessages: async (conversationId: string, token: string): Promise<ChatMessage[]> => {
    const response = await fetch(`${CHAT_API}/api/chat/conversations/${conversationId}/messages?token=${token}`)
    if (!response.ok) throw new Error('Failed to get messages')
    return response.json()
  },
}
