import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { chatApi, videoApi } from '../lib/api'
import { Send, ArrowLeft, FileText } from 'lucide-react'
import { formatTimestamp } from '../lib/utils'

export default function ChatPage() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const token = localStorage.getItem('token')
  const [message, setMessage] = useState('')
  const [selectedVideoId, setSelectedVideoId] = useState<string | undefined>()
  const [conversationId, setConversationId] = useState<string | undefined>()
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const { data: videos } = useQuery({
    queryKey: ['videos'],
    queryFn: () => videoApi.list(token!),
    enabled: !!token,
  })

  const { data: messages, isLoading } = useQuery({
    queryKey: ['messages', conversationId],
    queryFn: () => chatApi.getMessages(conversationId!, token!),
    enabled: !!conversationId && !!token,
  })

  const sendMessageMutation = useMutation({
    mutationFn: (data: { message: string; videoId?: string; conversationId?: string }) =>
      chatApi.send(data.message, token!, data.videoId, data.conversationId),
    onSuccess: (data) => {
      setConversationId(data.conversation_id)
      queryClient.invalidateQueries({ queryKey: ['messages', data.conversation_id] })
    },
  })

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault()
    if (!message.trim()) return

    sendMessageMutation.mutate({
      message,
      videoId: selectedVideoId,
      conversationId,
    })
    setMessage('')
  }

  if (!token) {
    navigate('/login')
    return null
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <button
                onClick={() => navigate('/dashboard')}
                className="flex items-center text-gray-700 hover:text-gray-900 mr-4"
              >
                <ArrowLeft className="w-5 h-5" />
              </button>
              <h1 className="text-xl font-bold text-gray-900">AI Chat</h1>
            </div>
            <button
              onClick={() => {
                localStorage.removeItem('token')
                localStorage.removeItem('user')
                navigate('/login')
              }}
              className="text-sm font-medium text-gray-700 hover:text-gray-900"
            >
              Logout
            </button>
          </div>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Video Selector */}
        {videos && videos.length > 0 && (
          <div className="mb-6 bg-white shadow rounded-lg p-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Video (Optional)
            </label>
            <select
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
              value={selectedVideoId || ''}
              onChange={(e) => setSelectedVideoId(e.target.value || undefined)}
            >
              <option value="">All Videos</option>
              {videos.filter(v => v.status === 'completed').map((video) => (
                <option key={video.id} value={video.id}>
                  {video.title}
                </option>
              ))}
            </select>
          </div>
        )}

        {/* Chat Messages */}
        <div className="bg-white shadow rounded-lg p-6 mb-4 h-[500px] overflow-y-auto">
          {!conversationId ? (
            <div className="text-center py-12">
              <FileText className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">Start a conversation</h3>
              <p className="mt-1 text-sm text-gray-500">
                Ask a question about your uploaded videos
              </p>
            </div>
          ) : isLoading ? (
            <div className="text-center py-8 text-gray-500">Loading messages...</div>
          ) : messages && messages.length > 0 ? (
            <div className="space-y-4">
              {messages.map((msg) => (
                <div
                  key={msg.id}
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg p-4 ${
                      msg.role === 'user'
                        ? 'bg-indigo-600 text-white'
                        : 'bg-gray-100 text-gray-900'
                    }`}
                  >
                    <p className="whitespace-pre-wrap">{msg.content}</p>
                    {msg.sources && msg.sources.length > 0 && (
                      <div className="mt-3 pt-3 border-t border-gray-300">
                        <p className="text-xs font-medium mb-2">Sources:</p>
                        {msg.sources.map((source, idx) => (
                          <div
                            key={idx}
                            className="text-xs bg-white bg-opacity-20 rounded p-2 mb-1"
                          >
                            <p className="font-medium">{source.video_title}</p>
                            <p className="opacity-80">@ {formatTimestamp(source.start_time)}</p>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
          ) : (
            <div className="text-center py-12 text-gray-500">
              No messages yet. Start by asking a question!
            </div>
          )}
        </div>

        {/* Message Input */}
        <form onSubmit={handleSend} className="bg-white shadow rounded-lg p-4">
          <div className="flex space-x-4">
            <input
              type="text"
              className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
              placeholder="Ask a question about your videos..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              disabled={sendMessageMutation.isPending}
            />
            <button
              type="submit"
              disabled={!message.trim() || sendMessageMutation.isPending}
              className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
