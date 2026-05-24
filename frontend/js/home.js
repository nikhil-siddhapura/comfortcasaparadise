// js/home.js
window.addEventListener("DOMContentLoaded", async () => {
  updateNavbar();
  await loadCategories();
  await loadProducts();
  await loadServices();
  await loadFeedback();
});

function updateNavbar() {
  if (isLoggedIn()) {
    document.getElementById("navGuest")?.classList.add("hidden");
    document.getElementById("navUser")?.classList.remove("hidden");
    document.getElementById("navLogout")?.classList.remove("hidden");
  }
}

async function loadCategories() {
  try {
    const cats = await CategoryAPI.getAll();
    const grid = document.getElementById("categoryGrid");
    const filterBar = document.getElementById("filterBar");
    if (!cats.length) { grid.innerHTML = `<p style="grid-column:1/-1;text-align:center;color:var(--muted)">No categories yet.</p>`; return; }
    grid.innerHTML = cats.map((c, i) => {
      const colors = ["#1a5276","#117a65","#6e2f8e","#7d6608","#1a5276"];
      const emojis = ["🏨","🛏️","🎪","💼","🏖️"];
      return `<div class="card" onclick="filterByCategory(${c.id},'${c.name}')" style="cursor:pointer">
        ${c.image
          ? `<img src="${imageUrl(c.image)}" class="card-img" alt="${c.name}" onerror="this.parentElement.querySelector('.fallback-ph').style.display='flex';this.style.display='none'"/>
             <div class="fallback-ph card-img-placeholder" style="background:${colors[i%5]};display:none">${emojis[i%5]}</div>`
          : `<div class="card-img-placeholder" style="background:${colors[i%5]}">${emojis[i%5]}</div>`}
        <div class="card-body">
          <div class="card-title">${c.name}</div>
          <div class="card-text">${c.description || "Premium category"}</div>
          <div class="card-price">${formatCurrency(c.price)} <span>/ night</span></div>
          <button class="btn btn-primary btn-sm">View Rooms</button>
        </div>
      </div>`;
    }).join("");
    filterBar.innerHTML = `<button class="btn btn-outline btn-sm" onclick="loadProducts(null)">All</button>` +
      cats.map(c => `<button class="btn btn-outline btn-sm" onclick="filterByCategory(${c.id},'${c.name}')">${c.name}</button>`).join("");
  } catch (err) {
    document.getElementById("categoryGrid").innerHTML = `<p style="color:var(--danger)">${err.message}</p>`;
  }
}

async function loadProducts(categoryId = null) {
  const grid = document.getElementById("productGrid");
  grid.innerHTML = `<div class="spinner"></div>`;
  try {
    const products = await ProductAPI.getAll(categoryId);
    if (!products.length) { grid.innerHTML = `<p style="grid-column:1/-1;text-align:center;color:var(--muted)">No rooms in this category.</p>`; return; }
    const emojis = ["🛏️","🏨","🌊","🌿","🏖️"];
    grid.innerHTML = products.map((p, i) => `
      <div class="card">
        ${p.image
          ? `<img src="${imageUrl(p.image)}" class="card-img" alt="${p.name}" onerror="this.nextElementSibling.style.display='flex';this.style.display='none'"/>
             <div class="card-img-placeholder" style="background:#1a5276;display:none">${emojis[i%5]}</div>`
          : `<div class="card-img-placeholder" style="background:#1a5276">${emojis[i%5]}</div>`}
        <div class="card-body">
          <div class="card-title">${p.name}</div>
          <div class="card-text">${p.description || ""}</div>
          <div class="card-price">${formatCurrency(p.price)} <span>/ night</span></div>
          <div style="font-size:0.82rem;color:var(--muted);margin-bottom:12px">🛏 ${p.available_rooms} of ${p.total_rooms} available</div>
          <a href="booking.html?product_id=${p.id}" class="btn btn-primary btn-sm btn-block">Book Now</a>
        </div>
      </div>`).join("");
  } catch (err) { grid.innerHTML = `<p style="color:var(--danger)">${err.message}</p>`; }
}

function filterByCategory(id, name) {
  document.getElementById("productsHeading").textContent = id ? `${name} — Rooms` : "All Rooms & Suites";
  document.getElementById("rooms").scrollIntoView({ behavior:"smooth" });
  loadProducts(id);
}

async function loadServices() {
  try {
    const services = await ServiceAPI.getAll();
    const grid = document.getElementById("serviceGrid");
    const emojis = ["💆","🍽️","✈️","💪","🛎️"];
    if (!services.length) { grid.innerHTML = `<p style="grid-column:1/-1;text-align:center;color:var(--muted)">No services yet.</p>`; return; }
    grid.innerHTML = services.map((s, i) => `
      <div class="card">
        ${s.image
          ? `<img src="${imageUrl(s.image)}" class="card-img" alt="${s.name}" onerror="this.nextElementSibling.style.display='flex';this.style.display='none'"/>
             <div class="card-img-placeholder" style="background:#117a65;display:none">${emojis[i%5]}</div>`
          : `<div class="card-img-placeholder" style="background:#117a65">${emojis[i%5]}</div>`}
        <div class="card-body">
          <div class="card-title">${s.name}</div>
          <div class="card-text">${s.description || ""}</div>
          <div class="card-price">${formatCurrency(s.price)}</div>
        </div>
      </div>`).join("");
  } catch (err) { document.getElementById("serviceGrid").innerHTML = ""; }
}

async function loadFeedback() {
  try {
    const list = await FeedbackAPI.getAll();
    const grid = document.getElementById("feedbackGrid");
    if (!list.length) { grid.innerHTML = `<p style="grid-column:1/-1;text-align:center;color:var(--muted)">No reviews yet.</p>`; return; }
    grid.innerHTML = list.slice(0, 6).map(f => `
      <div class="card">
        <div class="card-body">
          <div class="stars">${"⭐".repeat(f.rating)}</div>
          <div class="card-text mt-1" style="font-style:italic">"${f.comment || "Great experience!"}"</div>
          <div style="font-size:0.8rem;color:var(--muted);margin-top:10px">${formatDate(f.created_at)}</div>
        </div>
      </div>`).join("");
  } catch (err) { document.getElementById("feedbackGrid").innerHTML = ""; }
}

async function sendContact() {
  const name    = document.getElementById("cName").value.trim();
  const email   = document.getElementById("cEmail").value.trim();
  const subject = document.getElementById("cSubject").value.trim();
  const message = document.getElementById("cMessage").value.trim();
  if (!name || !email || !message) { showAlert("contactAlert","Name, email and message are required."); return; }
  try {
    await ContactAPI.send({ name, email, subject, message });
    showAlert("contactAlert","✅ Message sent! We'll get back to you soon.","success");
    ["cName","cEmail","cSubject","cMessage"].forEach(id => document.getElementById(id).value = "");
  } catch (err) { showAlert("contactAlert", err.message); }
}
