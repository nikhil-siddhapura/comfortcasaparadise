// js/admin/sidebar.js — inject sidebar dynamically
function getActivePage() { return window.location.pathname.split("/").pop(); }
function renderSidebar() {
  const page = getActivePage();
  const links = [
    { href:"dashboard.html",  icon:"📊", label:"Dashboard"  },
    { href:"categories.html", icon:"🏷️", label:"Categories" },
    { href:"products.html",   icon:"🛏️", label:"Products"   },
    { href:"bookings.html",   icon:"📅", label:"Bookings"   },
    { href:"users.html",      icon:"👥", label:"Users"      },
    { href:"contacts.html",   icon:"✉️", label:"Messages"   },
    { href:"services.html",   icon:"✨", label:"Services"   },
  ];
  return `
    <aside class="sidebar">
      <div class="sidebar-logo">🏨 <span>Royal Resort</span></div>
      <nav class="sidebar-nav">
        ${links.map(l => `
          <a href="${l.href}" class="${page===l.href?'active':''}">
            <span class="icon">${l.icon}</span><span>${l.label}</span>
          </a>`).join("")}
      </nav>
      <div class="sidebar-footer">
        <a href="../login.html" onclick="clearAuth()"><span class="icon">🚪</span><span>Logout</span></a>
      </div>
    </aside>`;
}
