// js/auth.js

function switchTab(tab) {
  const u = tab === "user";
  document.getElementById("userForm").classList.toggle("hidden", !u);
  document.getElementById("adminForm").classList.toggle("hidden", u);
  document.getElementById("tabUser").className = u
    ? "btn btn-primary btn-sm"
    : "btn btn-outline btn-sm";
  document.getElementById("tabAdmin").className = u
    ? "btn btn-outline btn-sm"
    : "btn btn-primary btn-sm";
}

async function loginUser() {
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;
  if (!email || !password) {
    showAlert("loginAlert", "Please fill in all fields.");
    return;
  }
  try {
    const data = await AuthAPI.login({ email, password });
    saveAuth(data.access_token, data.role);
    const user = await UserAPI.getMe();
    saveAuth(data.access_token, data.role, user.id);
    showAlert("loginAlert", "Login successful! Redirecting...", "success");
    setTimeout(() => (window.location.href = "index.html"), 1000);
  } catch (err) {
    showAlert("loginAlert", err.message);
  }
}

async function loginAdmin() {
  const username = document.getElementById("adminUsername").value.trim();
  const password = document.getElementById("adminPassword").value;
  if (!username || !password) {
    showAlert("loginAlert", "Please fill in all fields.");
    return;
  }
  try {
    const data = await AuthAPI.adminLogin({ username, password });
    saveAuth(data.access_token, data.role);
    showAlert("loginAlert", "Admin login successful!", "success");
    setTimeout(() => (window.location.href = "admin/dashboard.html"), 1000);
  } catch (err) {
    showAlert("loginAlert", err.message);
  }
}

async function registerUser() {
  const full_name = document.getElementById("regName").value.trim();
  const email = document.getElementById("regEmail").value.trim();
  const phone = document.getElementById("regPhone").value.trim();
  const password = document.getElementById("regPass").value;
  const confirm = document.getElementById("regPassConfirm").value;
  if (!full_name || !email || !password) {
    showAlert("regAlert", "Name, email and password are required.");
    return;
  }
  if (password !== confirm) {
    showAlert("regAlert", "Passwords do not match.");
    return;
  }
  if (password.length < 6) {
    showAlert("regAlert", "Password must be at least 6 characters.");
    return;
  }
  try {
    await AuthAPI.register({ full_name, email, phone, password });
    showAlert(
      "regAlert",
      "✅ Account created! Redirecting to login...",
      "success",
    );
    setTimeout(() => (window.location.href = "login.html"), 1500);
  } catch (err) {
    showAlert("regAlert", err.message);
  }
}

// Forgot password: get token
async function submitForgotPassword() {
  const email = document.getElementById("fpEmail").value.trim();
  if (!email) {
    showAlert("fpAlert", "Please enter your email address.");
    return;
  }
  try {
    const res = await AuthAPI.forgotPassword(email);
    // Show token on screen so user can copy-paste it into reset form
    document.getElementById("fpAlert").innerHTML = `
      <div class="alert alert-success">
        ✅ Token generated! Copy it below and paste in the Reset section.<br/><br/>
        <strong style="font-size:0.85rem;word-break:break-all;background:#eee;padding:6px 10px;border-radius:4px;display:block;">${res.token}</strong><br/>
        <span style="font-size:0.8rem;color:#555">⏰ Expires in 30 minutes</span>
      </div>`;
    // Auto-fill token in reset section
    document.getElementById("resetToken").value = res.token;
  } catch (err) {
    showAlert("fpAlert", err.message);
  }
}

// Reset password with token
async function submitResetPassword() {
  const token = document.getElementById("resetToken").value.trim();
  const password = document.getElementById("resetPass").value;
  const confirm = document.getElementById("resetConfirm").value;
  if (!token) {
    showAlert("resetAlert", "Please enter the reset token.");
    return;
  }
  if (!password) {
    showAlert("resetAlert", "Please enter a new password.");
    return;
  }
  if (password.length < 6) {
    showAlert("resetAlert", "Password must be at least 6 characters.");
    return;
  }
  if (password !== confirm) {
    showAlert("resetAlert", "Passwords do not match.");
    return;
  }
  try {
    await AuthAPI.resetPassword(token, password);
    showAlert(
      "resetAlert",
      "✅ Password reset successfully! Redirecting to login...",
      "success",
    );
    setTimeout(() => (window.location.href = "login.html"), 2000);
  } catch (err) {
    showAlert("resetAlert", err.message);
  }
}
