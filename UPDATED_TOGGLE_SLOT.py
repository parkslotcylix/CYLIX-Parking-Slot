# ============================================
# UPDATED toggle_slot() FUNCTION FOR app.py
# ============================================
# Replace the existing toggle_slot() function in app.py with this version
# This ensures parking_history is properly logged when slots change

@app.route('/api/toggle_slot', methods=['POST', 'OPTIONS'])
def toggle_slot():
    """
    Toggle parking slot status and log to parking_history
    Ensures database consistency and audit trail
    """
    try:
        data = request.get_json()
        slot_id = data.get('slot_id')
        
        if not slot_id:
            return jsonify({'success': False, 'error': 'slot_id is required'}), 400
        
        connection = get_db_connection()
        if connection is None:
            return jsonify({'success': False, 'error': 'Database connection failed'}), 500
        
        try:
            cursor = get_db_cursor(connection)
            
            # Get current slot status and check_in_time
            cursor.execute(
                "SELECT slot_status, check_in_time FROM parking_slots WHERE slot_id = %s",
                (slot_id,)
            )
            slot = cursor.fetchone()
            
            if not slot:
                cursor.close()
                return jsonify({'success': False, 'error': 'Slot not found'}), 404
            
            current_status = slot['slot_status']
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            if current_status == 'Available':
                # ===== TRANSITION: Available → Occupied =====
                new_status = 'Occupied'
                
                # 1. Update parking_slots table
                cursor.execute(
                    """UPDATE parking_slots 
                       SET slot_status = %s, check_in_time = %s, updated_at = %s 
                       WHERE slot_id = %s""",
                    (new_status, now, now, slot_id)
                )
                
                # 2. Create new history record
                cursor.execute(
                    """INSERT INTO parking_history 
                       (slot_id, check_in_time, status, created_at, updated_at) 
                       VALUES (%s, %s, %s, %s, %s)""",
                    (slot_id, now, 'active', now, now)
                )
                
            else:
                # ===== TRANSITION: Occupied → Available =====
                new_status = 'Available'
                check_out_time = now
                
                # 1. Update parking_slots table
                cursor.execute(
                    """UPDATE parking_slots 
                       SET slot_status = %s, check_out_time = %s, updated_at = %s 
                       WHERE slot_id = %s""",
                    (new_status, check_out_time, now, slot_id)
                )
                
                # 2. Get the active history record for this slot
                cursor.execute(
                    """SELECT history_id, check_in_time 
                       FROM parking_history 
                       WHERE slot_id = %s AND status = 'active' 
                       ORDER BY history_id DESC LIMIT 1""",
                    (slot_id,)
                )
                history = cursor.fetchone()
                
                # 3. Update history record if exists
                if history:
                    try:
                        check_in = datetime.strptime(history['check_in_time'], '%Y-%m-%d %H:%M:%S')
                        check_out = datetime.strptime(check_out_time, '%Y-%m-%d %H:%M:%S')
                        duration_hours = (check_out - check_in).total_seconds() / 3600
                        
                        cursor.execute(
                            """UPDATE parking_history 
                               SET check_out_time = %s, status = %s, duration_hours = %s, updated_at = %s
                               WHERE history_id = %s""",
                            (check_out_time, 'completed', duration_hours, now, history['history_id'])
                        )
                    except Exception as e:
                        print(f"Error calculating duration: {e}")
                        # Still mark as completed even if duration calculation fails
                        cursor.execute(
                            """UPDATE parking_history 
                               SET check_out_time = %s, status = %s, updated_at = %s
                               WHERE history_id = %s""",
                            (check_out_time, 'completed', now, history['history_id'])
                        )
            
            # Commit all changes in one transaction
            connection.commit()
            
            # 4. Log the action to admin_logs
            try:
                cursor.execute(
                    """INSERT INTO admin_logs 
                       (admin_id, action, slot_id, description, created_at) 
                       VALUES (%s, %s, %s, %s, %s)""",
                    (1, 'toggle_slot', slot_id, f'Status changed to {new_status}', now)
                )
                connection.commit()
            except Exception as e:
                print(f"Warning: Could not log action: {e}")
                # Don't fail the request if logging fails
            
            cursor.close()
            
            return jsonify({
                'success': True,
                'new_status': new_status,
                'timestamp': now,
                'slot_id': slot_id
            })
            
        except Exception as e:
            connection.rollback()
            print(f"Toggle slot error: {e}")
            cursor.close()
            return jsonify({'success': False, 'error': str(e)}), 500
        finally:
            connection.close()
            
    except Exception as e:
        print(f"Toggle slot outer error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================
# OPTIONAL: Batch Update Endpoint
# ============================================
# Add this endpoint to handle multiple slot updates efficiently

@app.route('/api/batch_update_slots', methods=['POST', 'OPTIONS'])
def batch_update_slots():
    """
    Update multiple slots in a single transaction
    Useful for camera-based detection or bulk operations
    
    Request body:
    {
        "updates": [
            {"slot_id": 1, "status": "Occupied"},
            {"slot_id": 2, "status": "Available"}
        ]
    }
    """
    try:
        data = request.get_json()
        updates = data.get('updates', [])
        
        if not updates:
            return jsonify({'success': False, 'error': 'No updates provided'}), 400
        
        if len(updates) > 100:
            return jsonify({'success': False, 'error': 'Maximum 100 slots per batch'}), 400
        
        connection = get_db_connection()
        if connection is None:
            return jsonify({'success': False, 'error': 'Database connection failed'}), 500
        
        try:
            cursor = get_db_cursor(connection)
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            updated_count = 0
            
            for update in updates:
                slot_id = update.get('slot_id')
                new_status = update.get('status')
                
                if not slot_id or not new_status:
                    continue
                
                if new_status not in ['Available', 'Occupied', 'Maintenance']:
                    continue
                
                try:
                    if new_status == 'Occupied':
                        # Update slot to occupied
                        cursor.execute(
                            """UPDATE parking_slots 
                               SET slot_status = %s, check_in_time = %s, updated_at = %s 
                               WHERE slot_id = %s""",
                            (new_status, now, now, slot_id)
                        )
                        
                        # Create history record
                        cursor.execute(
                            """INSERT INTO parking_history 
                               (slot_id, check_in_time, status, created_at, updated_at) 
                               VALUES (%s, %s, %s, %s, %s)""",
                            (slot_id, now, 'active', now, now)
                        )
                    else:
                        # Update slot to available or maintenance
                        cursor.execute(
                            """UPDATE parking_slots 
                               SET slot_status = %s, check_out_time = %s, updated_at = %s 
                               WHERE slot_id = %s""",
                            (new_status, now, now, slot_id)
                        )
                        
                        # Mark active history as completed
                        cursor.execute(
                            """UPDATE parking_history 
                               SET check_out_time = %s, status = %s, updated_at = %s
                               WHERE slot_id = %s AND status = 'active'""",
                            (now, 'completed', now, slot_id)
                        )
                    
                    updated_count += 1
                except Exception as e:
                    print(f"Error updating slot {slot_id}: {e}")
                    continue
            
            # Commit all changes
            connection.commit()
            cursor.close()
            
            return jsonify({
                'success': True,
                'message': f'Updated {updated_count} slots',
                'updated_count': updated_count,
                'timestamp': now
            })
            
        except Exception as e:
            connection.rollback()
            print(f"Batch update error: {e}")
            cursor.close()
            return jsonify({'success': False, 'error': str(e)}), 500
        finally:
            connection.close()
            
    except Exception as e:
        print(f"Batch update outer error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
