import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { videoApi, Video } from '../lib/api'
import { Upload, Video as VideoIcon, Trash2, MessageSquare } from 'lucide-react'

export default function Dashboard() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const token = localStorage.getItem('token')
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [title, setTitle] = useState('')
  const [uploading, setUploading] = useState(false)

  const { data: videos, isLoading } = useQuery({
    queryKey: ['videos'],
    queryFn: () => videoApi.list(token!),
    enabled: !!token,
  })

  const uploadMutation = useMutation({
    mutationFn: (data: { file: File; title: string }) =>
      videoApi.upload(data.file, data.title, token!),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['videos'] })
      setSelectedFile(null)
      setTitle('')
      setUploading(false)
    },
    onError: () => {
      setUploading(false)
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (videoId: string) => videoApi.delete(videoId, token!),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['videos'] })
    },
  })

  const handleUpload = (e: React.FormEvent) => {
    e.preventDefault()
    if (!selectedFile || !title) return

    setUploading(true)
    uploadMutation.mutate({ file: selectedFile, title })
  }

  const handleDelete = (videoId: string) => {
    if (window.confirm('Are you sure you want to delete this video?')) {
      deleteMutation.mutate(videoId)
    }
  }

  const getStatusColor = (status: Video['status']) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800'
      case 'processing':
        return 'bg-yellow-100 text-yellow-800'
      case 'failed':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
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
              <h1 className="text-xl font-bold text-gray-900">Vidyatrix AI</h1>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate('/chat')}
                className="flex items-center px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900"
              >
                <MessageSquare className="w-4 h-4 mr-2" />
                Chat
              </button>
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
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900">Upload Video</h2>
          <p className="mt-1 text-sm text-gray-500">
            Upload educational videos to ask questions about them
          </p>
        </div>

        <div className="bg-white shadow rounded-lg p-6 mb-8">
          <form onSubmit={handleUpload}>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Video Title
              </label>
              <input
                type="text"
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="Enter video title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
              />
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Video File
              </label>
              <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
                <div className="space-y-1 text-center">
                  <VideoIcon className="mx-auto h-12 w-12 text-gray-400" />
                  <div className="flex text-sm text-gray-600">
                    <label className="relative cursor-pointer bg-white rounded-md font-medium text-indigo-600 hover:text-indigo-500 focus-within:outline-none">
                      <span>Upload a file</span>
                      <input
                        type="file"
                        className="sr-only"
                        accept=".mp4,.mov,.avi,.mkv"
                        onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
                      />
                    </label>
                    <p className="pl-1">or drag and drop</p>
                  </div>
                  <p className="text-xs text-gray-500">MP4, MOV, AVI, MKV up to 500MB</p>
                  {selectedFile && (
                    <p className="text-sm text-indigo-600 mt-2">{selectedFile.name}</p>
                  )}
                </div>
              </div>
            </div>

            <button
              type="submit"
              disabled={!selectedFile || !title || uploading}
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
            >
              {uploading ? 'Uploading...' : 'Upload Video'}
            </button>
          </form>
        </div>

        <div>
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Your Videos</h2>
          {isLoading ? (
            <div className="text-center py-8 text-gray-500">Loading...</div>
          ) : videos && videos.length > 0 ? (
            <div className="grid gap-4">
              {videos.map((video) => (
                <div key={video.id} className="bg-white shadow rounded-lg p-6">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <h3 className="text-lg font-medium text-gray-900">{video.title}</h3>
                      <p className="text-sm text-gray-500">{video.filename}</p>
                      <div className="mt-2 flex items-center space-x-4">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(video.status)}`}>
                          {video.status}
                        </span>
                        {video.duration && (
                          <span className="text-sm text-gray-500">
                            {Math.floor(video.duration / 60)}:{Math.floor(video.duration % 60).toString().padStart(2, '0')}
                          </span>
                        )}
                      </div>
                      {video.error_message && (
                        <p className="mt-2 text-sm text-red-600">{video.error_message}</p>
                      )}
                    </div>
                    <button
                      onClick={() => handleDelete(video.id)}
                      className="ml-4 p-2 text-gray-400 hover:text-red-600"
                    >
                      <Trash2 className="w-5 h-5" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12 bg-white shadow rounded-lg">
              <VideoIcon className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">No videos</h3>
              <p className="mt-1 text-sm text-gray-500">
                Get started by uploading your first video
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
