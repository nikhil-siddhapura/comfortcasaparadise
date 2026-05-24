// js/booking.js
let products = [], services = [], selectedProduct = null;

window.addEventListener("DOMContentLoaded", async () => {
  if (!isLoggedIn()) { window.location.href = "login.html"; return; }
  const today = new Date().toISOString().split("T")[0];
  document.getElementById("checkIn").min  = today;
  document.getElementById("checkOut").min = today;
  await loadProducts();
  await loadServices();
  await loadMyBookings();
  const pid = new URLSearchParams(window.location.search).get("product_id");
  if (pid) { document.getElementById("productSelect").value = pid; onProductChange(); }
});

async function loadProducts() {
  products = await ProductAPI.getAll();
  const sel = document.getElementById("productSelect");
  sel.innerHTML = `<option value="">-- Choose a room --</option>` +
    products.map(p => `<option value="${p.id}">${p.name} — ${formatCurrency(p.price)}/night</option>`).join("");
}

async function loadServices() {
  services = await ServiceAPI.getAll();
  document.getElementById("servicesList").innerHTML = services.map(s => `
    <label style="display:flex;align-items:center;gap:6px;font-size:0.88rem;cursor:pointer;background:#f4f6f7;padding:7px 12px;border-radius:6px;border:1px solid #dce1e7">
      <input type="checkbox" value="${s.id}" class="svc-check" onchange="calcPrice()"/>
      ${s.name} <span style="color:var(--primary);font-weight:600">(+${formatCurrency(s.price)})</span>
    </label>`).join("");
}

function onProductChange() {
  const id = parseInt(document.getElementById("productSelect").value);
  selectedProduct = products.find(p => p.id === id) || null;
  document.getElementById("roomInfo").innerHTML = selectedProduct
    ? `<strong>${selectedProduct.name}</strong> &nbsp;|&nbsp; ${formatCurrency(selectedProduct.price)}/night &nbsp;|&nbsp; 🛏 ${selectedProduct.available_rooms} room(s) available`
    : "Select a room to see details.";
  calcPrice();
}

function calcPrice() {
  const inDate  = document.getElementById("checkIn").value;
  const outDate = document.getElementById("checkOut").value;
  const el = document.getElementById("priceSummary");
  if (!selectedProduct || !inDate || !outDate) { el.innerHTML = ""; return; }
  const nights = Math.max(0, (new Date(outDate) - new Date(inDate)) / 86400000);
  if (nights < 1) { el.innerHTML = `<p style="color:var(--danger)">Check-out must be after check-in.</p>`; return; }
  const roomTotal = selectedProduct.price * nights;
  const svcs = [...document.querySelectorAll(".svc-check:checked")]
    .map(cb => services.find(s => s.id === parseInt(cb.value))).filter(Boolean);
  const svcTotal = svcs.reduce((sum, s) => sum + parseFloat(s.price), 0);
  el.innerHTML = `
    <div style="display:grid;grid-template-columns:1fr auto;gap:6px;font-size:0.9rem;color:var(--text)">
      <span>Room × ${nights} night${nights!==1?"s":""}</span><strong>${formatCurrency(roomTotal)}</strong>
      <span>Extra Services</span><strong>${formatCurrency(svcTotal)}</strong>
      <span style="border-top:1px solid #eee;padding-top:6px;font-weight:700;color:var(--primary)">Total</span>
      <strong style="border-top:1px solid #eee;padding-top:6px;color:var(--primary);font-size:1.05rem">${formatCurrency(roomTotal+svcTotal)}</strong>
    </div>`;
}

function validatePersons() {
  const a = parseInt(document.getElementById("adults").value)   || 0;
  const c = parseInt(document.getElementById("children").value) || 0;
  document.getElementById("personsWarning").classList.toggle("hidden", a + c >= 3);
  calcPrice();
}

async function submitBooking() {
  const product_id = parseInt(document.getElementById("productSelect").value);
  const check_in   = document.getElementById("checkIn").value;
  const check_out  = document.getElementById("checkOut").value;
  const adults     = parseInt(document.getElementById("adults").value);
  const children   = parseInt(document.getElementById("children").value);
  if (!product_id)             { showAlert("bookAlert","Please select a room."); return; }
  if (!check_in || !check_out) { showAlert("bookAlert","Please select check-in and check-out dates."); return; }
  if (adults + children < 3)   { showAlert("bookAlert","Minimum 3 persons required (adults + children)."); return; }
  const service_ids = [...document.querySelectorAll(".svc-check:checked")].map(cb => parseInt(cb.value));
  try {
    await BookingAPI.create({ product_id, check_in, check_out, adults, children, service_ids });
    showAlert("bookAlert","✅ Booking submitted! Awaiting admin approval.","success");
    await loadMyBookings();
  } catch (err) { showAlert("bookAlert", err.message); }
}

async function loadMyBookings() {
  const el = document.getElementById("myBookings");
  try {
    const bookings = await BookingAPI.myBookings();
    if (!bookings.length) { el.innerHTML = `<p style="color:var(--muted)">No bookings yet.</p>`; return; }
    el.innerHTML = `<div class="table-wrap"><table>
      <thead><tr><th>ID</th><th>Room</th><th>Check-in</th><th>Check-out</th><th>Persons</th><th>Total</th><th>Status</th><th>Admin Note</th><th>Review</th></tr></thead>
      <tbody>${bookings.map(b => `
        <tr>
          <td>#${b.id}</td><td>#${b.product_id}</td>
          <td>${formatDate(b.check_in)}</td><td>${formatDate(b.check_out)}</td>
          <td>${b.adults+b.children}</td><td>${formatCurrency(b.total_price)}</td>
          <td><span class="badge badge-${b.status}">${b.status}</span></td>
          <td style="font-size:0.82rem;color:var(--muted);max-width:150px">${b.admin_message||"—"}</td>
          <td>${b.status==="approved"?`<button class="btn btn-sm btn-accent" onclick="openFeedback(${b.id})">⭐ Review</button>`:"—"}</td>
        </tr>`).join("")}
      </tbody></table></div>`;
  } catch (err) { el.innerHTML = `<p style="color:var(--danger)">${err.message}</p>`; }
}

function openFeedback(id) {
  document.getElementById("fbBookingId").value = id;
  document.getElementById("feedbackModal").classList.remove("hidden");
}
function closeFeedback() { document.getElementById("feedbackModal").classList.add("hidden"); }

async function submitFeedback() {
  const booking_id = parseInt(document.getElementById("fbBookingId").value);
  const rating     = parseInt(document.getElementById("fbRating").value);
  const comment    = document.getElementById("fbComment").value;
  try {
    await FeedbackAPI.submit({ booking_id, rating, comment });
    showAlert("feedbackAlert","✅ Review submitted! Thank you.","success");
    setTimeout(closeFeedback, 1500);
  } catch (err) { showAlert("feedbackAlert", err.message); }
}
