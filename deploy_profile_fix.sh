#!/bin/bash

# Deployment script for profile picture Supabase Storage fix

echo "🚀 Deploying Profile Picture Fix to Render..."
echo ""

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo "❌ Error: Not a git repository"
    exit 1
fi

# Show current status
echo "📋 Current Git Status:"
git status --short
echo ""

# Add changes
echo "➕ Adding changes..."
git add app.py PROFILE_PICTURE_FIX_COMPLETE.md deploy_profile_fix.sh
echo ""

# Commit
echo "💾 Committing changes..."
git commit -m "Fix: Use Supabase Storage for profile pictures (persist across restarts)

- Replace local filesystem upload with Supabase Storage
- Upload files to 'avatars' bucket via REST API
- Store public Supabase URLs in database
- Fixes ephemeral filesystem issue on Render free tier
- Images now persist across restarts"
echo ""

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push origin main
echo ""

echo "✅ Deployment initiated!"
echo ""
echo "📝 Next Steps:"
echo "1. Create Supabase Storage bucket 'avatars' (public)"
echo "2. Set storage policies (see PROFILE_PICTURE_FIX_COMPLETE.md)"
echo "3. Wait for Render auto-deploy to complete"
echo "4. Test upload at: https://cylix-parking-slot.onrender.com/account"
echo ""
echo "📖 Full instructions: PROFILE_PICTURE_FIX_COMPLETE.md"
