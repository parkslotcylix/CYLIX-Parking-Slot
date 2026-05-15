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
 * Refresh the shared profile UI from current session storage values
 */
function refreshSharedProfileUI() {
  const adminName = sessionStorage.getItem('user_name') || 'Admin User';
  const adminEmail = sessionStorage.getItem('user_email') || '';
  const accessLevel = sessionStorage.getItem('access_level') || 'admin';
  const status = sessionStorage.getItem('status') || 'active';
  const profilePicture = sessionStorage.getItem('profile_picture') || '/static/images/default-profile.png';

  const initials = getInitials(adminName);
  const roleBadge = getRoleBadge(accessLevel);
  const statusBadge = getStatusBadge(status);

  const profileAvatar = document.getElementById('profileAvatar');
  const profileName = document.getElementById('profileName');
  const profileInitials = document.getElementById('profileInitials');

  if (profileAvatar) {
    profileAvatar.src = profilePicture;
    profileAvatar.style.display = profilePicture ? 'block' : 'none';
    profileAvatar.onerror = function() {
      this.style.display = 'none';
      if (profileInitials) {
        profileInitials.textContent = initials;
        profileInitials.style.display = 'flex';
      }
    };
  }

  if (profileInitials) {
    profileInitials.textContent = initials;
    profileInitials.style.display = profilePicture ? 'none' : 'flex';
  }

  if (profileName) {
    profileName.textContent = adminName;
  }

  const dropdownAdminName = document.getElementById('dropdownAdminName');
  const dropdownAdminEmail = document.getElementById('dropdownAdminEmail');
  const dropdownRoleBadge = document.getElementById('dropdownRoleBadge');
  const dropdownStatusBadge = document.getElementById('dropdownStatusBadge');

  if (dropdownAdminName) dropdownAdminName.textContent = adminName;
  if (dropdownAdminEmail) dropdownAdminEmail.textContent = adminEmail;
  if (dropdownRoleBadge) dropdownRoleBadge.innerHTML = roleBadge;
  if (dropdownStatusBadge) dropdownStatusBadge.innerHTML = statusBadge;
}

window.refreshSharedProfileUI = refreshSharedProfileUI;

/**
 * Fetch user data from server and update profile picture if available
 * Ensures profile picture persists even after session storage is cleared
 */
function fetchAndUpdateProfilePicture() {
  const userEmail = sessionStorage.getItem('user_email');
  
  // Only fetch if user is logged in
  if (!userEmail) {
    return;
  }
  
  fetch(`${API_BASE}/api/me`, {
    method: 'GET',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => {
    if (response.ok) {
      return response.json();
    }
    throw new Error('Failed to fetch user data');
  })
  .then(data => {
    if (data.success && data.admin) {
      // Update session storage with latest data from server
      const profilePicture = data.admin.profile_picture || '/static/images/default-profile.png';
      sessionStorage.setItem('profile_picture', profilePicture);
      
      // Update UI with latest profile picture
      const profileAvatar = document.getElementById('profileAvatar');
      if (profileAvatar) {
        profileAvatar.src = profilePicture;
        profileAvatar.style.display = profilePicture ? 'block' : 'none';
      }
      
      const profileInitials = document.getElementById('profileInitials');
      if (profileInitials && profilePicture === '/static/images/default-profile.png') {
        const adminName = sessionStorage.getItem('user_name') || 'Admin User';
        profileInitials.textContent = getInitials(adminName);
        profileInitials.style.display = 'flex';
      } else if (profileInitials) {
        profileInitials.style.display = 'none';
      }
    }
  })
  .catch(error => {
    console.error('Error updating profile picture:', error);
    // Silently fail - use sessionStorage data if available
  });
}

/**
 * Initialize the profile dropdown component
 */
function initializeProfileDropdown() {
  // First refresh from session storage
  refreshSharedProfileUI();
  
  // Then fetch latest user data from server to ensure profile picture is current
  fetchAndUpdateProfilePicture();

  // Setup dropdown toggle
  const profileTrigger = document.getElementById('profileTrigger');
  const dropdownMenu = document.getElementById('dropdownMenu');

  if (profileTrigger && dropdownMenu) {
    // Add click handler
    profileTrigger.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      console.log('Profile trigger clicked');
      dropdownMenu.classList.toggle('show');
      console.log('Dropdown show class:', dropdownMenu.classList.contains('show'));
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
      if (!profileTrigger.contains(e.target) && !dropdownMenu.contains(e.target)) {
        dropdownMenu.classList.remove('show');
      }
    });
  } else {
    console.error('Profile dropdown elements not found:', {
      profileTrigger: !!profileTrigger,
      dropdownMenu: !!dropdownMenu
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
