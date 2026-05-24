// ============================================================
// js/api.js — Central API helper
// ============================================================
const API_BASE = "http://localhost:8000";

function getToken()   { return localStorage.getItem("token"); }
function getRole()    { return localStorage.getItem("role"); }
function isLoggedIn() { return !!getToken(); }
function isAdmin()    { return getRole() === "admin"; }
function isUser()     { return getRole() === "user"; }

function saveAuth(token, role, userId = null) {
  localStorage.setItem("token", token);
  localStorage.setItem("role",  role);
  if (userId) localStorage.setItem("user_id", userId);
}
function clearAuth() {
  localStorage.removeItem("token");
  localStorage.removeItem("role");
  localStorage.removeItem("user_id");
}

async function apiFetch(endpoint, options = {}) {
  const headers = { "Content-Type": "application/json", ...options.headers };
  const token   = getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;
  if (options.body instanceof FormData) delete headers["Content-Type"];
  const res  = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || "Something went wrong");
  return data;
}

// ── Auth ─────────────────────────────────────────────────────
const AuthAPI = {
  register:      (p)     => apiFetch("/auth/register",        { method:"POST", body: JSON.stringify(p) }),
  login:         (p)     => apiFetch("/auth/login",           { method:"POST", body: JSON.stringify(p) }),
  adminLogin:    (p)     => apiFetch("/auth/admin-login",     { method:"POST", body: JSON.stringify(p) }),
  forgotPassword:(email) => apiFetch("/auth/forgot-password", { method:"POST", body: JSON.stringify({ email }) }),
  resetPassword: (t, pw) => apiFetch("/auth/reset-password",  { method:"POST", body: JSON.stringify({ token:t, new_password:pw }) }),
};

// ── Categories ────────────────────────────────────────────────
const CategoryAPI = {
  getAll:      ()       => apiFetch("/categories/"),                                          // public: active only
  getAllAdmin:  ()       => apiFetch("/categories/admin/all"),                                 // admin: all including inactive
  getOne:      (id)     => apiFetch(`/categories/${id}`),
  create:      (form)   => apiFetch("/categories/",           { method:"POST",   body: form }),
  update:      (id, p)  => apiFetch(`/categories/${id}`,      { method:"PUT",    body: JSON.stringify(p) }),
  updateImage: (id, form)=> apiFetch(`/categories/${id}/image`,{ method:"PUT",   body: form }),
  delete:      (id)     => apiFetch(`/categories/${id}`,      { method:"DELETE" }),
};

// ── Products ──────────────────────────────────────────────────
const ProductAPI = {
  getAll:      (catId)  => apiFetch(`/products/${catId ? `?category_id=${catId}` : ""}`),     // public
  getAllAdmin:  ()       => apiFetch("/products/admin/all"),                                    // admin: all
  getOne:      (id)     => apiFetch(`/products/${id}`),
  create:      (form)   => apiFetch("/products/",             { method:"POST",   body: form }),
  update:      (id, p)  => apiFetch(`/products/${id}`,        { method:"PUT",    body: JSON.stringify(p) }),
  updateImage: (id, form)=> apiFetch(`/products/${id}/image`, { method:"PUT",    body: form }),
  delete:      (id)     => apiFetch(`/products/${id}`,        { method:"DELETE" }),
};

// ── Bookings ──────────────────────────────────────────────────
const BookingAPI = {
  create:       (p)     => apiFetch("/bookings/",              { method:"POST", body: JSON.stringify(p) }),
  myBookings:   ()      => apiFetch("/bookings/my"),
  allBookings:  ()      => apiFetch("/bookings/"),
  updateStatus: (id, p) => apiFetch(`/bookings/${id}/status`,  { method:"PUT",  body: JSON.stringify(p) }),
};

// ── Feedback ──────────────────────────────────────────────────
const FeedbackAPI = {
  submit: (p) => apiFetch("/feedback/", { method:"POST", body: JSON.stringify(p) }),
  getAll: ()  => apiFetch("/feedback/"),
};

// ── Contacts ──────────────────────────────────────────────────
const ContactAPI = {
  send:   (p)          => apiFetch("/contacts/",             { method:"POST", body: JSON.stringify(p) }),
  getAll: ()           => apiFetch("/contacts/"),
  reply:  (id, reply)  => apiFetch(`/contacts/${id}/reply`,  { method:"PUT",  body: JSON.stringify({ admin_reply: reply }) }),
};

// ── Services ──────────────────────────────────────────────────
const ServiceAPI = {
  getAll:      ()       => apiFetch("/services/"),                                             // public
  getAllAdmin:  ()       => apiFetch("/services/admin/all"),                                    // admin: all
  create:      (form)   => apiFetch("/services/",             { method:"POST",   body: form }),
  update:      (id, p)  => apiFetch(`/services/${id}`,        { method:"PUT",    body: JSON.stringify(p) }),
  updateImage: (id, form)=> apiFetch(`/services/${id}/image`, { method:"PUT",    body: form }),
  delete:      (id)     => apiFetch(`/services/${id}`,        { method:"DELETE" }),
};

// ── Users ─────────────────────────────────────────────────────
const UserAPI = {
  getMe:       ()      => apiFetch("/users/me"),
  updateMe:    (p)     => apiFetch("/users/me",         { method:"PUT",  body: JSON.stringify(p) }),
  uploadAvatar:(form)  => apiFetch("/users/me/avatar",  { method:"POST", body: form }),
  getAllUsers:  ()      => apiFetch("/users/"),
};

// ── UI Helpers ────────────────────────────────────────────────
function showAlert(id, msg, type = "error") {
  const el = document.getElementById(id);
  if (!el) return;
  el.innerHTML = `<div class="alert alert-${type}">${msg}</div>`;
  setTimeout(() => { if (el) el.innerHTML = ""; }, 6000);
}
function showSpinner(id) {
  const el = document.getElementById(id);
  if (el) el.innerHTML = `<div class="spinner"></div>`;
}
function imageUrl(path) {
  if (!path) return null;
  if (path.startsWith("http")) return path;
  return `${API_BASE}/${path}`;
}
function formatDate(d) {
  return new Date(d).toLocaleDateString("en-IN", { day:"numeric", month:"short", year:"numeric" });
}
function formatCurrency(n) {
  return `₹${parseFloat(n).toLocaleString("en-IN")}`;
}
function toggleNav() {
  document.getElementById("navLinks").classList.toggle("open");
}
function logout() { clearAuth(); window.location.href = "/index.html"; }
function adminLogout() { clearAuth(); window.location.href = "../login.html"; }
