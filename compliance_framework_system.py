
#!/usr/bin/env python3
"""
Quantum Security System - Backup and Restore System
Copyright © 2025 Ervin Remus Radosavlevici
Official Owner: Ervin Remus Radosavlevici
Contact: radosavlevici210@icloud.com
Official Timestamp: 2025-06-02T00:30:00Z
Private and Public Repository Rights Reserved
Licensed under MIT License with additional copyright protections
All rights reserved.
"""

from flask import request, jsonify
import json
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class BackupSystem:
    def __init__(self, backup_dir="backup"):
        self.backup_dir = backup_dir
        self.data_file = os.path.join(backup_dir, "quantum_data.json")
        self.settings_file = os.path.join(backup_dir, "system_settings.json")
        
        # Ensure backup directory exists
        os.makedirs(backup_dir, exist_ok=True)
        
        # Initialize data store
        self.data_store = self.load_data()
        self.settings_store = self.load_settings()
        
    def load_data(self):
        """Load quantum data from backup file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load data: {e}")
                return {}
        return {}
    
    def load_settings(self):
        """Load system settings from backup file"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load settings: {e}")
                return self.get_default_settings()
        return self.get_default_settings()
    
    def get_default_settings(self):
        """Get default system settings"""
        return {
            "quantum_encryption": True,
            "neural_defense": True,
            "crystal_matrix_stability": 99.7,
            "neural_electrodes": 15750,
            "thought_reading_accuracy": 96.8,
            "security_level": "MAXIMUM",
            "auto_backup": True,
            "backup_interval": 3600,
            "owner": "Ervin Remus Radosavlevici",
            "contact": "radosavlevici210@icloud.com",
            "copyright": "© 2025 Ervin Remus Radosavlevici",
            "last_backup": None,
            "last_restore": None
        }
    
    def save_data(self):
        """Save quantum data to backup file"""
        try:
            with open(self.data_file, "w") as f:
                json.dump(self.data_store, f, indent=2)
            logger.info("Quantum data backup completed successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to save data: {e}")
            return False
    
    def save_settings(self):
        """Save system settings to backup file"""
        try:
            self.settings_store["last_backup"] = datetime.utcnow().isoformat()
            with open(self.settings_file, "w") as f:
                json.dump(self.settings_store, f, indent=2)
            logger.info("System settings backup completed successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
            return False
    
    def restore_all_to_defaults(self):
        """Restore all settings to default values"""
        try:
            self.settings_store = self.get_default_settings()
            self.settings_store["last_restore"] = datetime.utcnow().isoformat()
            self.data_store = {}
            
            # Save the restored defaults
            self.save_data()
            self.save_settings()
            
            logger.info("All systems restored to default settings")
            return True
        except Exception as e:
            logger.error(f"Failed to restore defaults: {e}")
            return False

# Initialize backup system
backup_system = BackupSystem()

def register_backup_routes(app):
    """Register backup and restore routes with the Flask app"""
    
    @app.route('/api/backup/data', methods=['GET', 'POST'])
    def api_backup_data():
        """API endpoint for quantum data backup and retrieval"""
        try:
            if request.method == 'POST':
                data = request.get_json()
                if not data:
                    return jsonify({'error': 'No data provided'}), 400
                
                key = data.get('key')
                value = data.get('value')
                
                if not key:
                    return jsonify({'error': 'Key is required'}), 400
                
                backup_system.data_store[key] = value
                backup_system.save_data()
                
                logger.info(f"Quantum data saved: {key}")
                return jsonify({
                    'status': 'saved',
                    'key': key,
                    'timestamp': datetime.utcnow().isoformat(),
                    'copyright': '© 2025 Ervin Remus Radosavlevici'
                }), 201
            
            # GET request - return all data
            return jsonify({
                'data': backup_system.data_store,
                'total_entries': len(backup_system.data_store),
                'last_backup': backup_system.settings_store.get('last_backup'),
                'copyright': '© 2025 Ervin Remus Radosavlevici'
            })
            
        except Exception as e:
            logger.error(f"Backup data error: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/backup/manual', methods=['POST'])
    def api_manual_backup():
        """API endpoint for manual backup"""
        try:
            data_saved = backup_system.save_data()
            settings_saved = backup_system.save_settings()
            
            if data_saved and settings_saved:
                return jsonify({
                    'status': 'manual backup completed',
                    'timestamp': datetime.utcnow().isoformat(),
                    'data_entries': len(backup_system.data_store),
                    'copyright': '© 2025 Ervin Remus Radosavlevici'
                })
            else:
                return jsonify({'error': 'Backup failed'}), 500
                
        except Exception as e:
            logger.error(f"Manual backup error: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/restore/data', methods=['POST'])
    def api_restore_data():
        """API endpoint for data restoration"""
        try:
            if os.path.exists(backup_system.data_file):
                backup_system.data_store = backup_system.load_data()
                backup_system.settings_store["last_restore"] = datetime.utcnow().isoformat()
                backup_system.save_settings()
                
                logger.info("Quantum data restored successfully")
                return jsonify({
                    'status': 'restored',
                    'entries_restored': len(backup_system.data_store),
                    'timestamp': datetime.utcnow().isoformat(),
                    'copyright': '© 2025 Ervin Remus Radosavlevici'
                })
            else:
                return jsonify({'error': 'No backup found'}), 404
                
        except Exception as e:
            logger.error(f"Restore data error: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/restore/defaults', methods=['POST'])
    def api_restore_defaults():
        """API endpoint for restoring all systems to default settings"""
        try:
            if backup_system.restore_all_to_defaults():
                return jsonify({
                    'status': 'all systems restored to defaults',
                    'quantum_encryption': True,
                    'neural_defense': True,
                    'crystal_matrix_stability': 99.7,
                    'neural_electrodes': 15750,
                    'thought_reading_accuracy': 96.8,
                    'security_level': 'MAXIMUM',
                    'timestamp': datetime.utcnow().isoformat(),
                    'owner': 'Ervin Remus Radosavlevici',
                    'contact': 'radosavlevici210@icloud.com',
                    'copyright': '© 2025 Ervin Remus Radosavlevici'
                })
            else:
                return jsonify({'error': 'Failed to restore defaults'}), 500
                
        except Exception as e:
            logger.error(f"Restore defaults error: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/backup/settings', methods=['GET', 'POST'])
    def api_backup_settings():
        """API endpoint for system settings backup and retrieval"""
        try:
            if request.method == 'POST':
                data = request.get_json()
                if data:
                    # Update settings with provided data
                    for key, value in data.items():
                        if key not in ['owner', 'contact', 'copyright']:  # Protect immutable fields
                            backup_system.settings_store[key] = value
                    
                    backup_system.save_settings()
                    
                    return jsonify({
                        'status': 'settings updated',
                        'timestamp': datetime.utcnow().isoformat(),
                        'copyright': '© 2025 Ervin Remus Radosavlevici'
                    })
            
            # GET request - return current settings
            return jsonify({
                'settings': backup_system.settings_store,
                'copyright': '© 2025 Ervin Remus Radosavlevici'
            })
            
        except Exception as e:
            logger.error(f"Backup settings error: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/backup-dashboard')
    def backup_dashboard():
        """Backup and restore dashboard page"""
        try:
            return f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Quantum Security Backup System</title>
                <style>
                    body {{ font-family: 'Courier New', monospace; background: #000; color: #00ff00; margin: 0; padding: 20px; }}
                    .container {{ max-width: 1200px; margin: 0 auto; }}
                    .header {{ text-align: center; margin-bottom: 30px; }}
                    .section {{ background: rgba(0, 255, 0, 0.1); border: 1px solid #00ff00; margin: 20px 0; padding: 20px; border-radius: 5px; }}
                    .button {{ background: #00ff00; color: #000; padding: 10px 20px; border: none; cursor: pointer; margin: 5px; border-radius: 3px; }}
                    .button:hover {{ background: #00cc00; }}
                    .status {{ margin: 10px 0; padding: 10px; background: rgba(0, 255, 0, 0.2); border-radius: 3px; }}
                    .data-display {{ background: #001100; padding: 15px; border-radius: 5px; white-space: pre-wrap; max-height: 300px; overflow-y: auto; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🛡️ QUANTUM SECURITY BACKUP SYSTEM 🛡️</h1>
                        <p>© 2025 Ervin Remus Radosavlevici - Official Owner</p>
                        <p>📧 Contact: radosavlevici210@icloud.com</p>
                    </div>
                    
                    <div class="section">
                        <h2>🔄 Backup Operations</h2>
                        <button class="button" onclick="manualBackup()">Manual Backup</button>
                        <button class="button" onclick="viewData()">View Data</button>
                        <button class="button" onclick="viewSettings()">View Settings</button>
                        <div id="backup-status" class="status"></div>
                    </div>
                    
                    <div class="section">
                        <h2>🔧 Restore Operations</h2>
                        <button class="button" onclick="restoreData()">Restore Data</button>
                        <button class="button" onclick="restoreDefaults()">Restore All to Defaults</button>
                        <div id="restore-status" class="status"></div>
                    </div>
                    
                    <div class="section">
                        <h2>📊 Data Management</h2>
                        <input type="text" id="data-key" placeholder="Enter key" style="padding: 10px; margin: 5px;">
                        <input type="text" id="data-value" placeholder="Enter value" style="padding: 10px; margin: 5px;">
                        <button class="button" onclick="saveData()">Save Data</button>
                        <div id="data-status" class="status"></div>
                    </div>
                    
                    <div class="section">
                        <h2>📋 System Information</h2>
                        <div id="system-info" class="data-display">Loading system information...</div>
                    </div>
                </div>
                
                <script>
                    async function manualBackup() {{
                        try {{
                            const response = await fetch('/api/backup/manual', {{ method: 'POST' }});
                            const result = await response.json();
                            document.getElementById('backup-status').textContent = JSON.stringify(result, null, 2);
                        }} catch (error) {{
                            document.getElementById('backup-status').textContent = 'Error: ' + error.message;
                        }}
                    }}
                    
                    async function viewData() {{
                        try {{
                            const response = await fetch('/api/backup/data');
                            const result = await response.json();
                            document.getElementById('backup-status').textContent = JSON.stringify(result, null, 2);
                        }} catch (error) {{
                            document.getElementById('backup-status').textContent = 'Error: ' + error.message;
                        }}
                    }}
                    
                    async function viewSettings() {{
                        try {{
                            const response = await fetch('/api/backup/settings');
                            const result = await response.json();
                            document.getElementById('backup-status').textContent = JSON.stringify(result, null, 2);
                        }} catch (error) {{
                            document.getElementById('backup-status').textContent = 'Error: ' + error.message;
                        }}
                    }}
                    
                    async function restoreData() {{
                        try {{
                            const response = await fetch('/api/restore/data', {{ method: 'POST' }});
                            const result = await response.json();
                            document.getElementById('restore-status').textContent = JSON.stringify(result, null, 2);
                        }} catch (error) {{
                            document.getElementById('restore-status').textContent = 'Error: ' + error.message;
                        }}
                    }}
                    
                    async function restoreDefaults() {{
                        if (confirm('This will restore all settings to defaults. Continue?')) {{
                            try {{
                                const response = await fetch('/api/restore/defaults', {{ method: 'POST' }});
                                const result = await response.json();
                                document.getElementById('restore-status').textContent = JSON.stringify(result, null, 2);
                            }} catch (error) {{
                                document.getElementById('restore-status').textContent = 'Error: ' + error.message;
                            }}
                        }}
                    }}
                    
                    async function saveData() {{
                        const key = document.getElementById('data-key').value;
                        const value = document.getElementById('data-value').value;
                        
                        if (!key || !value) {{
                            document.getElementById('data-status').textContent = 'Please enter both key and value';
                            return;
                        }}
                        
                        try {{
                            const response = await fetch('/api/backup/data', {{
                                method: 'POST',
                                headers: {{ 'Content-Type': 'application/json' }},
                                body: JSON.stringify({{ key, value }})
                            }});
                            const result = await response.json();
                            document.getElementById('data-status').textContent = JSON.stringify(result, null, 2);
                            document.getElementById('data-key').value = '';
                            document.getElementById('data-value').value = '';
                        }} catch (error) {{
                            document.getElementById('data-status').textContent = 'Error: ' + error.message;
                        }}
                    }}
                    
                    // Load system information on page load
                    window.onload = async function() {{
                        try {{
                            const response = await fetch('/api/system-status');
                            const result = await response.json();
                            document.getElementById('system-info').textContent = JSON.stringify(result, null, 2);
                        }} catch (error) {{
                            document.getElementById('system-info').textContent = 'Error loading system info: ' + error.message;
                        }}
                    }};
                </script>
            </body>
            </html>
            """
        except Exception as e:
            logger.error(f"Backup dashboard error: {e}")
            return jsonify({'error': str(e)}), 500
