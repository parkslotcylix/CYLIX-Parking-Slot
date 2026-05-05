// Authentication and Access Control
// This script checks user session and controls navigation visibility

const API_BASE = window.location.origin + '/api';

// Check session and update navigation
async function checkSessionAndUpdateNav() {
    try {
        const response = await fetch(`${API_BASE}/check_session`);
        const data = await response.json();
        
        if (data.logged_in) {
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
