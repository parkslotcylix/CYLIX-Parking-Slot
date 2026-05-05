// Authentication and Access Control
// This script checks user session and controls navigation visibility

const API_BASE = window.location.origin + '/api';

// Check session and update navigation
async function checkSessionAndUpdateNav() {
    try {
        const response = await fetch(`${API_BASE}/check_session`);
        const data = await response.json();
        
        if (data.logged_in) {
            // Update profile display in navigation
            updateProfileDisplay(data);
            
            // Hide Admin Management link if not super admin
            const adminManagementLinks = document.querySelectorAll('a[href="/admin-management"]');
            adminManagementLinks.forEach(link => {
                if (data.access_level !== 'super_admin') {
                    link.parentElement.style.display = 'none';
                } else {
                    link.parentElement.style.display = 'list-item';
                }
            });
            
            // Check if account is inactive or suspended
            if (data.status === 'inactive') {
                showStatusWarning('Your account is inactive. Please contact the administrator.');
            } else if (data.status === 'suspended') {
                showStatusWarning('Your account is suspended. Please contact the administrator.');
            }
        } else {
            // Not logged in - hide admin management link
            const adminManagementLinks = document.querySelectorAll('a[href="/admin-management"]');
            adminManagementLinks.forEach(link => {
                link.parentElement.style.display = 'none';
            });
        }
    } catch (error) {
        console.error('Session check error:', error);
        // Hide admin management link on error
        const adminManagementLinks = document.querySelectorAll('a[href="/admin-management"]');
        adminManagementLinks.forEach(link => {
            link.parentElement.style.display = 'none';
        });
    }
}

// Update profile display in navigation
async function updateProfileDisplay(sessionData) {
    try {
        // Get admin details including profile picture
        const response = await fetch(`${API_BASE}/get_admin`);
        const data = await response.json();
        
        if (data.success && data.admin) {
            const admin = data.admin;
            const profilePicture = admin.profile_picture || '/static/images/default-profile.png';
            const adminName = sessionData.user_name || admin.admin_name || 'Admin';
            
            // Find all account links and replace with profile display
            const accountLinks = document.querySelectorAll('a[href="/account"]');
            accountLinks.forEach(link => {
                // Create profile display
                const profileHTML = `
                    <a href="/account" class="nav-profile-link" style="display: flex; align-items: center; gap: 8px; text-decoration: none; color: rgba(255,255,255,0.8); transition: color 0.2s;">
                        <img src="${profilePicture}" 
                             alt="${adminName}" 
                             onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\\'http://www.w3.org/2000/svg\\' viewBox=\\'0 0 100 100\\'%3E%3Crect fill=\\'%237FB77E\\' width=\\'100\\' height=\\'100\\'/%3E%3Ccircle cx=\\'50\\' cy=\\'35\\' r=\\'20\\' fill=\\'%23fff\\'/%3E%3Cpath d=\\'M 15 75 Q 15 60 50 60 Q 85 60 85 75 L 85 100 L 15 100 Z\\' fill=\\'%23fff\\'/%3E%3C/svg%3E'"
                             style="width: 32px; height: 32px; border-radius: 50%; object-fit: cover; border: 2px solid rgba(255,255,255,0.3); transition: border-color 0.2s;" />
                        <span style="font-weight: 700; font-size: 0.88rem; letter-spacing: 0.06em; text-transform: uppercase;">${adminName}</span>
                    </a>
                `;
                
                link.outerHTML = profileHTML;
            });
            
            // Add hover effect for profile links
            setTimeout(() => {
                const profileLinks = document.querySelectorAll('.nav-profile-link');
                profileLinks.forEach(profileLink => {
                    profileLink.addEventListener('mouseenter', function() {
                        this.style.color = '#f5c842';
                        const img = this.querySelector('img');
                        if (img) img.style.borderColor = '#f5c842';
                    });
                    profileLink.addEventListener('mouseleave', function() {
                        this.style.color = 'rgba(255,255,255,0.8)';
                        const img = this.querySelector('img');
                        if (img) img.style.borderColor = 'rgba(255,255,255,0.3)';
                    });
                });
            }, 100);
        }
    } catch (error) {
        console.error('Profile display error:', error);
    }
}

// Show status warning banner
function showStatusWarning(message) {
    // Check if warning already exists
    if (document.getElementById('status-warning-banner')) {
        return;
    }
    
    const banner = document.createElement('div');
    banner.id = 'status-warning-banner';
    banner.style.cssText = `
        position: fixed;
        top: 68px;
        left: 0;
        right: 0;
        background: #fff3cd;
        border-bottom: 3px solid #ffc107;
        padding: 15px 20px;
        text-align: center;
        z-index: 999;
        font-family: 'Nunito', sans-serif;
        font-weight: 700;
        color: #856404;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    `;
    
    banner.innerHTML = `
        <span style="margin-right: 10px;">⚠️</span>
        ${message}
        <button onclick="this.parentElement.remove()" style="
            background: none;
            border: none;
            color: #856404;
            font-size: 1.2rem;
            cursor: pointer;
            margin-left: 15px;
            font-weight: bold;
        ">&times;</button>
    `;
    
    document.body.insertBefore(banner, document.body.firstChild);
    
    // Adjust main content padding to account for banner
    const mainContent = document.querySelector('.container') || document.querySelector('section');
    if (mainContent) {
        mainContent.style.marginTop = '20px';
    }
}

// Run on page load
document.addEventListener('DOMContentLoaded', () => {
    checkSessionAndUpdateNav();
});
