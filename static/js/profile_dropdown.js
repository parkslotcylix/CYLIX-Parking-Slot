/**
 * Profile Dropdown Component
 * Displays logged-in admin with dropdown menu
 * Handles authentication, role-based access, and logout
 */

// Initialize profile dropdown on page load
document.addEventListener('DOMContentLoaded', () => {
  initializeProfileDropdown();
  checkAuthenticationAndRole();
});

/**
 * Initialize the profile dropdown component
 */
function initializeProfileDropdown() {
  // Get session data
  const adminName = sessionStorage.getItem('user_name') || 'Admin User';
  const adminEmail = sessionStorage.getItem('user_email') || '';
  const accessLevel = sessionStorage.getItem('access_level') || 'admin';
  const status = sessionStorage.getItem('status') || 'active';
  const profilePicture = sessionStorage.getItem('profile_picture') || '/static/images/default-profile.png';

  // Get initials for fallback
  const initials = getInitials(adminName);

  // Get role badge
  const roleBadge = getRoleBadge(accessLevel);
  
  // Get status badge
  const statusBadge = getStatusBadge(status);

  // Update profile trigger
  const profileAvatar = document.getElementById('profileAvatar');
  const profileName = document.getElementById('profileName');
  const profileInitials = document.getElementById('profileInitials');

  if (profileAvatar) {
    profileAvatar.src = profilePicture;
    profileAvatar.onerror = function() {
      // If image fails to load, hide image and show initials
      this.style.display = 'none';
      if (profileInitials) {
        profileInitials.textContent = initials;
        profileInitials.style.display = 'flex';
      }
    };
  }

  if (profileInitials) {
    profileInitials.textContent = initials;
  }

  if (profileName) {
    profileName.textContent = adminName;
  }

  // Update dropdown content
  document.getElementById('dropdownAdminName').textContent = adminName;
  document.getElementById('dropdownAdminEmail').textContent = adminEmail;
  document.getElementById('dropdownRoleBadge').innerHTML = roleBadge;
  document.getElementById('dropdownStatusBadge').innerHTML = statusBadge;

  // Setup dropdown toggle
  const profileTrigger = document.getElementById('profileTrigger');
  const dropdownMenu = document.getElementById('dropdownMenu');

  if (profileTrigger && dropdownMenu) {
    profileTrigger.addEventListener('click', (e) => {
      e.stopPropagation();
      dropdownMenu.classList.toggle('show');
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
      if (!profileTrigger.contains(e.target) && !dropdownMenu.contains(e.target)) {
        dropdownMenu.classList.remove('show');
      }
    });
  }

  // Hide Admin Management link if not super_admin
  hideAdminManagementIfNotSuperAdmin();
}

/**
 * Get initials from name
 */
function getInitials(name) {
  if (!name) return 'A';
  const parts = name.trim().split(' ');
  if (parts.length >= 2) {
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
  }
  return name[0].toUpperCase();
}

/**
 * Get role badge HTML
 */
function getRoleBadge(accessLevel) {
  const badges = {
    'super_admin': '<span class="role-badge super-admin">⭐ Super Admin</span>',
    'admin': '<span class="role-badge admin">🔐 Admin</span>',
    'manager': '<span class="role-badge manager">📋 Manager</span>'
  };
  return badges[accessLevel] || badges['admin'];
}

/**
 * Get status badge HTML
 */
function getStatusBadge(status) {
  const badges = {
    'active': '<span class="status-badge active"><span class="status-dot"></span> Active</span>',
    'inactive': '<span class="status-badge inactive"><span class="status-dot"></span> Inactive</span>',
    'suspended': '<span class="status-badge suspended"><span class="status-dot"></span> Suspended</span>'
  };
  return badges[status] || badges['active'];
}

/**
 * Check authentication and redirect if not logged in
 */
function checkAuthenticationAndRole() {
  const userEmail = sessionStorage.getItem('user_email');
  const accessLevel = sessionStorage.getItem('access_level');

  // Check if logged in
  if (!userEmail) {
    window.location.href = '/';
    return;
  }

  // Check role-based access for Admin Management page
  const currentPath = window.location.pathname;
  if (currentPath === '/admin-management' && accessLevel !== 'super_admin') {
    alert('Access Denied. Super Admin privileges required.');
    window.location.href = '/home';
    return;
  }
}

/**
 * Hide Admin Management link if not super_admin
 */
function hideAdminManagementIfNotSuperAdmin() {
  const accessLevel = sessionStorage.getItem('access_level');
  if (accessLevel !== 'super_admin') {
    const adminManagementLinks = document.querySelectorAll('a[href="/admin-management"]');
    adminManagementLinks.forEach(link => {
      const listItem = link.closest('li');
      if (listItem) {
        listItem.style.display = 'none';
      }
    });
  }
}

/**
 * Handle logout
 */
async function handleLogout(event) {
  if (event) event.preventDefault();
  
  if (confirm('Are you sure you want to logout?')) {
    try {
      // Call backend logout endpoint to clear server-side session
      await fetch(`${API_BASE}/api/logout`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include'
      });
    } catch (error) {
      console.error('Logout error:', error);
    }
    
    // Clear all client-side storage
    sessionStorage.clear();
    
    // Redirect to home page
    window.location.href = '/';
  }
}
