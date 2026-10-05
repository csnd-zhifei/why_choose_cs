import axios from 'axios'

// 开发期由 vite 代理到后端，生产可改为完整地址
const http = axios.create({ baseURL: '', timeout: 60000 })

// 统一把后端的 {"detail": "..."} 抛成 Error
http.interceptors.response.use(
  (res) => res,
  (err) => {
    const detail = err.response?.data?.detail || err.message || '请求失败'
    return Promise.reject(new Error(detail))
  },
)

function formData(file) {
  const fd = new FormData()
  fd.append('file', file)
  return fd
}

export const api = {
  // ---- 用户 ----
  register: (data) => http.post('/api/v1/users/register', data).then((r) => r.data),
  login: (data) => http.post('/api/v1/users/login', data).then((r) => r.data),
  getUser: (id) => http.get(`/api/v1/users/${id}`).then((r) => r.data),
  updateUser: (id, data) => http.patch(`/api/v1/users/${id}`, data).then((r) => r.data),
  uploadAvatar: (id, file) =>
    http.post(`/api/v1/users/${id}/avatar`, formData(file)).then((r) => r.data),

  // ---- 笔记 ----
  listPosts: (params) => http.get('/api/v1/books', { params }).then((r) => r.data),
  getPost: (id) => http.get(`/api/v1/books/${id}`).then((r) => r.data),
  createPost: (data) => http.post('/api/v1/books', data).then((r) => r.data),
  updatePost: (id, data) => http.patch(`/api/v1/books/${id}`, data).then((r) => r.data),
  deletePost: (id) => http.delete(`/api/v1/books/${id}`).then((r) => r.data),
  listBookmarks: (params) =>
    http.get('/api/v1/books/bookmarks', { params }).then((r) => r.data),
  uploadMd: (id, file) =>
    http.post(`/api/v1/books/${id}/md`, formData(file)).then((r) => r.data),
  uploadHtml: (id, file) =>
    http.post(`/api/v1/books/${id}/html`, formData(file)).then((r) => r.data),
  toggleLike: (id, userid) =>
    http.post(`/api/v1/books/${id}/like`, null, { params: { userid } }).then((r) => r.data),
  toggleBookmark: (id, userid) =>
    http.post(`/api/v1/books/${id}/bookmark`, null, { params: { userid } }).then((r) => r.data),

  // ---- 评论 ----
  listComments: (postid) =>
    http.get('/api/v1/comments', { params: { postid } }).then((r) => r.data),
  createComment: (data) => http.post('/api/v1/comments', data).then((r) => r.data),
  deleteComment: (id) => http.delete(`/api/v1/comments/${id}`).then((r) => r.data),
  listReplies: (commentid) =>
    http.get(`/api/v1/comments/${commentid}/replies`).then((r) => r.data),
  createReply: (commentid, data) =>
    http.post(`/api/v1/comments/${commentid}/replies`, data).then((r) => r.data),
  deleteReply: (id) => http.delete(`/api/v1/comments/replies/${id}`).then((r) => r.data),
}

export default api
