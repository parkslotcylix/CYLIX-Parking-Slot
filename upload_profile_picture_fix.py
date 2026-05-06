# Replace the upload_profile_picture function in app.py with this code

@app.route('/api/upload_profile_picture', methods=['POST', 'OPTIONS'])
def upload_profile_picture():
    try:
        if request.method == 'OPTIONS':
            return '', 200
        
        # Check if file exists in request
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        admin_id = request.form.get('admin_id')
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Invalid file type. Allowed: png, jpg, jpeg, gif, webp'}), 400
        
        # Read file content
        file_content = file.read()
        
        if len(file_content) > MAX_FILE_SIZE:
            return jsonify({'success': False, 'error': 'File size exceeds 5MB limit'}), 400
        
        # Generate secure filename
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"admin_{admin_id}_{int(time.time())}.{ext}"
        
        # Upload to Supabase Storage
        storage_path = f"profile-pictures/{filename}"
        
        try:
            # Upload file to Supabase Storage using REST API
            upload_url = f"{SUPABASE_URL}/storage/v1/object/avatars/{storage_path}"
            
            upload_headers = {
                'Authorization': f'Bearer {SUPABASE_API_KEY}',
                'Content-Type': f'image/{ext}',
                'apikey': SUPABASE_API_KEY
            }
            
            upload_response = requests.post(
                upload_url,
                headers=upload_headers,
                data=file_content,
                timeout=30
            )
            
            if upload_response.status_code not in [200, 201]:
                print(f"Supabase storage upload failed: {upload_response.status_code} - {upload_response.text}")
                return jsonify({'success': False, 'error': 'Failed to upload to storage'}), 500
            
            # Get public URL
            picture_url = f"{SUPABASE_URL}/storage/v1/object/public/avatars/{storage_path}"
            
        except Exception as storage_error:
            print(f"Storage error: {storage_error}")
            return jsonify({'success': False, 'error': 'Storage upload failed'}), 500
        
        # Update database with new picture URL
        try:
            update_resp = requests.patch(
                f"{SUPABASE_URL}/rest/v1/admin",
                headers={**SUPABASE_HEADERS, 'Prefer': 'return=representation'},
                params={'admin_id': f'eq.{admin_id}'},
                json={'profile_picture': picture_url},
                timeout=10
            )
            
            if update_resp.status_code not in [200, 204]:
                return jsonify({'success': False, 'error': 'Failed to update database'}), 500
            
            return jsonify({
                'success': True,
                'picture_url': picture_url,
                'message': 'Profile picture updated successfully'
            })
            
        except Exception as db_error:
            print(f"Database update error: {db_error}")
            return jsonify({'success': False, 'error': 'Database update failed'}), 500
            
    except Exception as e:
        print(f"Upload error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
