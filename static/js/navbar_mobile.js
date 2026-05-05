/**
 * Mobile Navbar Functionality
 * Handles hamburger menu toggle and mobile navigation
 */

document.addEventListener('DOMContentLoaded', function() {
  initializeMobileNavbar();
  updateMobileProfile();
});

/**
 * Initialize mobile navbar functionality
 */
function initializeMobileNavbar() {
  const navbarToggle = document.getElementById('navbarToggle');
  const mobileMenu = document.getElementById('navbarMobileMenu');
  
  if (!navbarToggle || !mobileMenu) {
    console.warn('Mobile navbar elements not found');
    return;
  }

  // Toggle mobile menu
  navbarToggle.addEventListener('click', function() {
    toggleMobileMenu();
  });

  // Close mobile menu when clicking on a link
  const mobileLinks = mobileMenu.querySelectorAll('a');
  mobileLinks.forEach(link => {
    link.addEventListener('click', function() {
      closeMobileMenu();
    });
  });

  // Close mobile menu when clicking outside
  document.addEventListener('click', function(event) {
    const isClickInsideNav = navbarToggle.contains(event.target) || mobileMenu.contains(event.target);
    if (!isClickInsideNav && mobileMenu.classList.contains('active')) {
      closeMobileMenu();
    }
  });

  // Close mobile menu on escape key
  document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape' && mobileMenu.classList.contains('active')) {
      closeMobileMenu();
    }
  });

  // Handle window resize
  window.addEventListener('resize', function() {
    if (window.innerWidth > 768 && mobileMenu.classList.contains('active')) {
      closeMobileMenu();
    }
  });

  // Set active link based on current page
  setActiveNavLink();
}

/**
 * Toggle mobile menu open/closed
 */
function toggleMobileMenu() {
  const navbarToggle = document.getElementById('navbarToggle');
  const mobileMenu = document.getElementById('navbarMobileMenu');
  
  navbarToggle.classList.toggle('active');
  mobileMenu.classList.toggle('active');
  
  // Prevent body scroll when menu is open
  if (mobileMenu.classList.contains('active')) {
    document.body.style.overflow = 'hidden';
  } else {
    document.body.style.overflow = '';
  }
}

/**
 * Close mobile menu
 */
function closeMobileMenu() {
  const navbarToggle = document.getElementById('navbarToggle');
  const mobileMenu = document.getElementById('navbarMobileMenu');
  
  navbarToggle.classList.remove('active');
  mobileMenu.classList.remove('active');
  document.body.style.overflow = '';
}

/**
 * Set active navigation link based on current page
 */
function setActiveNavLink() {
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.navbar-nav a, .mobile-nav-links a');
  
  navLinks.forEach(link => {
    link.classList.remove('active');
    const linkPath = new URL(link.href).pathname;
    
    if (linkPath === currentPath) {
      link.classList.add('active');
    }
  });
}

/**
 * Update mobile profile section with current user data
 */
function updateMobileProfile() {
  // Get session data
  const adminName = sessionStorage.getItem('user_name') || 'Admin User';
  const adminEmail = sessionStorage.getItem('user_email') || '';
  const accessLevel = sessionStorage.getItem('access_level') || 'admin';
  const status = sessionStorage.getItem('status') || 'active';
  const profilePicture = sessionStorage.getItem('profile_picture') || '/static/images/default-profile.png';

  // Get initials for fallback
  const initials = getInitials(adminName);

  // Get role and status badges
  const roleBadge = getRoleBadge(accessLevel);
  const statusBadge = getStatusBadge(status);

  // Update mobile profile elements
  const mobileProfileAvatar = document.getElementById('mobileProfileAvatar');
  const mobileProfileName = document.getElementById('mobileProfileName');
  const mobileProfileEmail = document.getElementById('mobileProfileEmail');
  const mobileProfileBadges = document.getElementById('mobileProfileBadges');

  if (mobileProfileAvatar) {
    mobileProfileAvatar.textContent = initials;
  }

  if (mobileProfileName) {
    mobileProfileName.textContent = adminName;
  }

  if (mobileProfileEmail) {
    mobileProfileEmail.textContent = adminEmail;
  }

  if (mobileProfileBadges) {
    mobileProfileBadges.innerHTML = roleBadge + statusBadge;
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
 * Handle logout from mobile menu
 */
async function handleMobileLogout(event) {
  event.preventDefault();
  
  if (confirm('Are you sure you want to logout?')) {
    try {
      // Call backend logout endpoint
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
    
    // Close mobile menu and redirect
    closeMobileMenu();
    window.location.href = '/';
  }
}

// Export functions for global use
window.toggleMobileMenu = toggleMobileMenu;
window.closeMobileMenu = closeMobileMenu;
window.handleMobileLogout = handleMobileLogout;