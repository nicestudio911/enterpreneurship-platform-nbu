import { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { getProject, updateProject, deleteProject } from '../api/projects'
import { generateFiles, getProjectFiles, downloadFile, downloadAllFiles, getGenerationLogs, getFileContent, regenerateSingleFile, type GeneratedFile, type GenerationLog, type FileContent } from '../api/files'
import type { Project } from '../api/projects'
import './ProjectView.css'

function ProjectView() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [project, setProject] = useState<Project | null>(null)
  const [files, setFiles] = useState<GeneratedFile[]>([])
  const [logs, setLogs] = useState<GenerationLog[]>([])
  const [loading, setLoading] = useState(true)
  const [generating, setGenerating] = useState(false)
  const [error, setError] = useState('')
  const [isEditing, setIsEditing] = useState(false)
  const [editedDescription, setEditedDescription] = useState('')
  const [saving, setSaving] = useState(false)
  const [previewFile, setPreviewFile] = useState<FileContent | null>(null)
  const [loadingPreview, setLoadingPreview] = useState(false)
  const [regeneratingFile, setRegeneratingFile] = useState<string | null>(null)
  const [deleting, setDeleting] = useState(false)
  const logsEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const loadProject = async () => {
      if (!id) {
        setError('Project ID is required')
        setLoading(false)
        return
      }

      try {
        const projectId = parseInt(id, 10)
        if (isNaN(projectId)) {
          setError('Invalid project ID')
          setLoading(false)
          return
        }

        const data = await getProject(projectId)
        setProject(data)
        setEditedDescription(data.idea_description || '')
        
        // Check if files exist
        await checkFiles(projectId)
      } catch (err: any) {
        if (err.response?.status === 404) {
          setError('Project not found')
        } else {
          setError('Failed to load project')
        }
        console.error('Error loading project:', err)
      } finally {
        setLoading(false)
      }
    }

    loadProject()
  }, [id])

  const scrollToBottom = () => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [logs])

  const checkFiles = async (projectId: number) => {
    try {
      const projectFiles = await getProjectFiles(projectId)
      // Sort files by created_at descending to show newest first
      const sortedFiles = [...projectFiles].sort((a, b) => 
        new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      )
      setFiles(sortedFiles)
      
      // Load existing logs
      await loadLogs(projectId)
      
      // If no files exist, start generation
      if (projectFiles.length === 0) {
        await startFileGeneration(projectId)
      } else {
        // Check if any files are still generating
        const hasGenerating = projectFiles.some(f => f.status === 'generating' || f.status === 'pending')
        if (hasGenerating) {
          setGenerating(true)
          pollForFiles(projectId)
        }
      }
    } catch (err) {
      console.error('Error checking files:', err)
    }
  }

  const loadLogs = async (projectId: number) => {
    try {
      const projectLogs = await getGenerationLogs(projectId)
      setLogs(projectLogs)
    } catch (err) {
      console.error('Error loading logs:', err)
    }
  }

  const startFileGeneration = async (projectId: number) => {
    setGenerating(true)
    try {
      await generateFiles(projectId)
      // Poll for files
      pollForFiles(projectId)
    } catch (err: any) {
      setError('Failed to start file generation. Please try again.')
      console.error('Error generating files:', err)
      setGenerating(false)
    }
  }

  const pollForFiles = async (projectId: number) => {
    const maxAttempts = 120 // Poll for up to 10 minutes (5 second intervals)
    let attempts = 0

    const poll = async () => {
      try {
        // Poll for both files and logs
        const [projectFiles, projectLogs] = await Promise.all([
          getProjectFiles(projectId),
          getGenerationLogs(projectId)
        ])
        
        // Sort files by created_at descending to show newest first
        const sortedFiles = [...projectFiles].sort((a, b) => 
          new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        )
        setFiles(sortedFiles)
        setLogs(projectLogs)
        
        const hasGenerating = projectFiles.some(f => f.status === 'generating' || f.status === 'pending')
        const hasCompleted = projectFiles.some(f => f.status === 'completed')
        const hasError = projectFiles.some(f => f.status === 'failed')
        
        if (!hasGenerating && (hasCompleted || hasError)) {
          setGenerating(false)
          setRegeneratingFile(null) // Clear regenerating state
          return
        }
        
        if (attempts < maxAttempts) {
          attempts++
          setTimeout(poll, 2000) // Poll every 2 seconds for more responsive updates
        } else {
          setGenerating(false)
          setError('File generation is taking longer than expected. Please refresh the page.')
        }
      } catch (err) {
        console.error('Error polling for files:', err)
        setGenerating(false)
      }
    }

    poll()
  }

  const handleDownloadFile = async (fileId: number, filename: string) => {
    try {
      const blob = await downloadFile(fileId)
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = filename
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (err) {
      console.error('Error downloading file:', err)
      setError('Failed to download file. Please try again.')
    }
  }

  const handleDownloadAll = async () => {
    if (!id) return
    
    try {
      const projectId = parseInt(id, 10)
      const blob = await downloadAllFiles(projectId)
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `project_${projectId}_files.zip`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (err) {
      console.error('Error downloading all files:', err)
      setError('Failed to download files. Please try again.')
    }
  }

  const handleEdit = () => {
    setIsEditing(true)
    setEditedDescription(project?.idea_description || '')
  }

  const handleCancelEdit = () => {
    setIsEditing(false)
    setEditedDescription(project?.idea_description || '')
  }

  const handleSave = async () => {
    if (!id || !project) return
    
    setSaving(true)
    setError('')
    
    try {
      const projectId = parseInt(id, 10)
      const updatedProject = await updateProject(projectId, {
        idea_description: editedDescription
      })
      setProject(updatedProject)
      setIsEditing(false)
    } catch (err: any) {
      console.error('Error updating project:', err)
      setError('Failed to update project. Please try again.')
    } finally {
      setSaving(false)
    }
  }

  const handleRegenerateFiles = async () => {
    if (!id) return
    
    if (!window.confirm('This will delete all existing files and generate new ones. Are you sure?')) {
      return
    }
    
    try {
      const projectId = parseInt(id, 10)
      // Reset all states before starting new generation
      setGenerating(false)
      setError('')
      setFiles([])
      setLogs([])
      setPreviewFile(null) // Close preview if open
      setRegeneratingFile(null) // Clear any single file regeneration state
      // Small delay to ensure state is reset before starting
      await new Promise(resolve => setTimeout(resolve, 100))
      await startFileGeneration(projectId)
    } catch (err) {
      console.error('Error regenerating files:', err)
      setError('Failed to regenerate files. Please try again.')
      setGenerating(false)
    }
  }

  const handleViewFile = async (fileId: number) => {
    setLoadingPreview(true)
    setError('')
    try {
      const content = await getFileContent(fileId)
      setPreviewFile(content)
    } catch (err) {
      console.error('Error loading file content:', err)
      setError('Failed to load file content. Please try again.')
    } finally {
      setLoadingPreview(false)
    }
  }

  const handleClosePreview = () => {
    setPreviewFile(null)
  }

  const handleDeleteProject = async () => {
    if (!id) return
    
    if (!window.confirm('Are you sure you want to delete this project? This will permanently delete the project and all associated files. This action cannot be undone.')) {
      return
    }
    
    setDeleting(true)
    setError('')
    
    try {
      const projectId = parseInt(id, 10)
      await deleteProject(projectId)
      navigate('/dashboard')
    } catch (err: any) {
      console.error('Error deleting project:', err)
      setError('Failed to delete project. Please try again.')
      setDeleting(false)
    }
  }

  const handleRegenerateSingleFile = async (filename: string) => {
    if (!id) return
    
    if (!window.confirm(`Regenerate ${filename}? This will replace the existing file.`)) {
      return
    }
    
    setRegeneratingFile(filename)
    setError('')
    
    try {
      const projectId = parseInt(id, 10)
      await regenerateSingleFile(projectId, filename)
      // Start polling for updates
      setGenerating(true)
      pollForFiles(projectId)
    } catch (err: any) {
      console.error('Error regenerating file:', err)
      setError('Failed to regenerate file. Please try again.')
      setRegeneratingFile(null)
    }
  }

  if (loading) {
    return (
      <div className="project-view-container">
        <div className="loading-state">
          <div className="spinner" style={{ margin: '0 auto' }}></div>
          <p style={{ marginTop: '1rem' }}>Loading project...</p>
        </div>
      </div>
    )
  }

  if (error && !project) {
    return (
      <div className="project-view-container">
        <div className="alert alert-error">{error}</div>
      </div>
    )
  }

  if (!project) {
    return (
      <div className="project-view-container">
        <div className="alert alert-error">Project not found</div>
      </div>
    )
  }

  const completedFiles = files.filter(f => f.status === 'completed')

  return (
    <div className="project-view-container">
      <div className="project-header">
        <div className="project-header-content">
          <h1>{project.name}</h1>
        </div>
        <div className="project-header-actions">
          {!isEditing ? (
            <>
              <button onClick={handleEdit} className="btn-primary btn-sm" type="button">
                Edit Description
              </button>
              <button 
                onClick={handleDeleteProject} 
                className="btn-danger btn-sm"
                disabled={deleting}
                type="button"
              >
                {deleting ? 'Deleting...' : 'Delete Project'}
              </button>
            </>
          ) : (
            <div className="description-actions">
              <button 
                onClick={handleSave} 
                className="save-btn"
                disabled={saving}
                type="button"
              >
                {saving ? 'Saving...' : 'Save Changes'}
              </button>
              <button 
                onClick={handleCancelEdit} 
                className="cancel-btn"
                disabled={saving}
                type="button"
              >
                Cancel
              </button>
            </div>
          )}
        </div>
      </div>
      
      <div className="project-info-card">
        <div className="project-info-header">
          <div>
            <h3 className="project-info-title">Project Details</h3>
            <div className="project-info-meta">
              <span>Created: {new Date(project.created_at).toLocaleDateString()}</span>
            </div>
          </div>
        </div>
        
        <div className="project-description-section">
          <div className="project-description-label">Idea Description</div>
          {isEditing ? (
            <textarea
              value={editedDescription}
              onChange={(e) => setEditedDescription(e.target.value)}
              className="idea-description-textarea"
              rows={8}
              placeholder="Describe your project idea..."
            />
          ) : (
            <div className="project-description-content">
              {project.idea_description || 'No description provided.'}
            </div>
          )}
        </div>
      </div>

      <div className="files-section">
        <div className="files-header">
          <h2>Generated Files</h2>
          <div className="files-header-actions">
            {completedFiles.length > 0 ? (
              <>
                <button 
                  onClick={handleRegenerateFiles} 
                  className="regenerate-btn" 
                  disabled={generating || deleting}
                  type="button"
                >
                  {generating ? 'Regenerating...' : 'Regenerate All'}
                </button>
                <button 
                  onClick={handleDownloadAll} 
                  className="download-all-btn"
                  type="button"
                >
                  Download All
                </button>
              </>
            ) : (
              <button 
                onClick={() => id && startFileGeneration(parseInt(id, 10))} 
                className="btn-primary"
                disabled={generating || deleting}
                type="button"
              >
                {generating ? 'Generating...' : 'Generate Files'}
              </button>
            )}
          </div>
        </div>

        {generating && (
          <div className="generation-status">
            <div className="generating-header">
              <div className="spinner"></div>
              <h3>Generating Files...</h3>
            </div>
            <div className="logs-container">
              {logs.length === 0 ? (
                <p className="logs-placeholder">Waiting for generation to start...</p>
              ) : (
                <div className="logs-list">
                  {logs.map((log) => (
                    <div key={log.id} className={`log-entry log-${log.log_type}`}>
                      <span className="log-time">
                        {new Date(log.created_at).toLocaleTimeString()}
                      </span>
                      <span className="log-message">{log.message}</span>
                    </div>
                  ))}
                  <div ref={logsEndRef} />
                </div>
              )}
            </div>
          </div>
        )}

        {error && (
          <div className="alert alert-error">{error}</div>
        )}

        {!generating && completedFiles.length === 0 && files.length === 0 && (
          <div className="empty-state">
            <div className="empty-state-icon">📄</div>
            <h3>No files generated yet</h3>
            <p>Files will appear here once generation is complete.</p>
          </div>
        )}

        {completedFiles.length > 0 && (
          <div className="files-list">
            {completedFiles.map((file) => (
              <div key={file.id} className="file-item">
                <div className="file-info">
                  <span className="file-icon">📄</span>
                  <div className="file-details">
                    <span className="file-name">{file.filename}</span>
                    <span className="file-type">{file.file_type}</span>
                    <span className="file-date">Generated: {new Date(file.created_at).toLocaleString()}</span>
                  </div>
                </div>
                <div className="file-actions">
                  <button
                    onClick={() => handleViewFile(file.id)}
                    className="view-btn"
                    disabled={loadingPreview}
                  >
                    {loadingPreview ? 'Loading...' : 'View'}
                  </button>
                  <button
                    onClick={() => handleRegenerateSingleFile(file.filename)}
                    className="regenerate-single-btn"
                    disabled={regeneratingFile === file.filename || generating}
                    title="Regenerate this file"
                  >
                    {regeneratingFile === file.filename ? 'Regenerating...' : '🔄'}
                  </button>
                  <button
                    onClick={() => handleDownloadFile(file.id, file.filename)}
                    className="download-btn"
                  >
                    Download
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {previewFile && (
          <div className="file-preview-modal" onClick={handleClosePreview}>
            <div className="file-preview-content" onClick={(e) => e.stopPropagation()}>
              <div className="file-preview-header">
                <h3>{previewFile.filename}</h3>
                <button onClick={handleClosePreview} className="close-preview-btn">×</button>
              </div>
              <div className="file-preview-body">
                {previewFile.file_type === 'md' ? (
                  <div className="markdown-preview">
                    <ReactMarkdown 
                      remarkPlugins={[remarkGfm]}
                      components={{
                        h1: ({node, ...props}) => <h1 className="markdown-h1" {...props} />,
                        h2: ({node, ...props}) => <h2 className="markdown-h2" {...props} />,
                        h3: ({node, ...props}) => <h3 className="markdown-h3" {...props} />,
                        h4: ({node, ...props}) => <h4 className="markdown-h4" {...props} />,
                        h5: ({node, ...props}) => <h5 className="markdown-h5" {...props} />,
                        h6: ({node, ...props}) => <h6 className="markdown-h6" {...props} />,
                        p: ({node, ...props}) => <p className="markdown-p" {...props} />,
                        ul: ({node, ...props}) => <ul className="markdown-ul" {...props} />,
                        ol: ({node, ...props}) => <ol className="markdown-ol" {...props} />,
                        li: ({node, ...props}) => <li className="markdown-li" {...props} />,
                        code: ({node, inline, ...props}: any) => 
                          inline ? (
                            <code className="markdown-code-inline" {...props} />
                          ) : (
                            <code className="markdown-code-block" {...props} />
                          ),
                        pre: ({node, ...props}) => <pre className="markdown-pre" {...props} />,
                        blockquote: ({node, ...props}) => <blockquote className="markdown-blockquote" {...props} />,
                        strong: ({node, ...props}) => <strong className="markdown-strong" {...props} />,
                        em: ({node, ...props}) => <em className="markdown-em" {...props} />,
                        hr: ({node, ...props}) => <hr className="markdown-hr" {...props} />,
                        table: ({node, ...props}) => <table className="markdown-table" {...props} />,
                        thead: ({node, ...props}) => <thead className="markdown-thead" {...props} />,
                        tbody: ({node, ...props}) => <tbody className="markdown-tbody" {...props} />,
                        tr: ({node, ...props}) => <tr className="markdown-tr" {...props} />,
                        th: ({node, ...props}) => <th className="markdown-th" {...props} />,
                        td: ({node, ...props}) => <td className="markdown-td" {...props} />,
                      }}
                    >
                      {previewFile.content}
                    </ReactMarkdown>
                  </div>
                ) : (
                  <pre className="file-preview-text">{previewFile.content}</pre>
                )}
              </div>
            </div>
          </div>
        )}

        {files.some(f => f.status === 'failed') && (
          <div className="error">
            Some files failed to generate. Please try again or contact support.
          </div>
        )}
      </div>
    </div>
  )
}

export default ProjectView
