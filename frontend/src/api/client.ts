import axios from 'axios'

// Determine the base URL
// In production (Docker), ALWAYS use relative path which nginx will proxy
// This ensures requests go through the same origin (no CORS issues)
const getBaseURL = (): string => {
  // Always use relative path in production (when served through nginx)
  // This ensures requests go to the same origin (localhost:3000) and are proxied by nginx
  // Only use VITE_API_URL in development mode (when running npm run dev)
  if (import.meta.env.DEV && import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL
  }
  // Default to relative path - nginx will proxy /api to backend
  // This prevents cross-origin requests (localhost:3000 -> localhost:8080)
  return '/api'
}

const baseURL = getBaseURL()
console.log('API Client initialized with baseURL:', baseURL)

const apiClient = axios.create({
  baseURL: baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 second timeout
  withCredentials: false, // Don't send credentials for CORS
  validateStatus: function (status) {
    // Accept any status code as a valid response (don't throw on 4xx/5xx)
    return status >= 200 && status < 600;
  },
})

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  
  // Ensure we're using the correct URL format
  const fullURL = (config.baseURL || '') + (config.url || '')
  
  // Log the request being made
  console.log('API Request:', {
    method: config.method?.toUpperCase(),
    url: config.url,
    baseURL: config.baseURL,
    fullURL: fullURL,
    data: config.data,
    headers: config.headers,
  })
  
  // Validate the URL is correct
  if (!fullURL.startsWith('/api')) {
    console.warn('Warning: API URL does not start with /api:', fullURL)
  }
  
  return config
}, (error) => {
  console.error('Request interceptor error:', error)
  return Promise.reject(error)
})

// Add response interceptor for better error logging and 401 handling
apiClient.interceptors.response.use(
  (response) => {
    // Check for 401 Unauthorized even in successful responses (due to validateStatus)
    if (response.status === 401) {
      // Clear invalid token
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      // Redirect to login
      if (window.location.pathname !== '/login' && window.location.pathname !== '/signup') {
        window.location.href = '/login'
      }
      return Promise.reject(new Error('Unauthorized: Invalid or expired token'))
    }
    return response
  },
  (error) => {
    // Handle 401 errors from network errors or other cases
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      if (window.location.pathname !== '/login' && window.location.pathname !== '/signup') {
        window.location.href = '/login'
      }
    }
    
    console.error('API Error:', {
      message: error.message,
      url: error.config?.url,
      baseURL: error.config?.baseURL,
      fullURL: error.config?.baseURL + error.config?.url,
      status: error.response?.status,
      data: error.response?.data,
      request: error.request,
    })
    return Promise.reject(error)
  }
)

export default apiClient
