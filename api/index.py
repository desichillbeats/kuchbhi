from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add parent directory to path to import sigma_study_v4
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    import sigma_study_v4
    import requests
except Exception as e:
    sigma_study_v4 = None
    requests = None
    import_error = str(e)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            'message': 'Sigma Study API - use POST /api with JSON body containing link',
            'status': 'ok'
        }
        self.wfile.write(json.dumps(response).encode())
        return
    
    def do_POST(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            link = data.get('link', '')
            
            if not link:
                self.end_headers()
                error_response = {'success': False, 'error': 'Missing link parameter'}
                self.wfile.write(json.dumps(error_response).encode())
                return
            
            # Check if modules loaded
            if not sigma_study_v4 or not requests:
                self.end_headers()
                error_response = {'success': False, 'error': f'Import error: {import_error}'}
                self.wfile.write(json.dumps(error_response).encode())
                return
            
            # Validate supported domains
            supported_domains = ['nanolinks', 'arolinks', 'lksfy']
            if not any(domain in link for domain in supported_domains):
                self.end_headers()
                error_response = {
                    'success': False,
                    'error': 'Unsupported domain. Use links from nanolinks.com, arolinks.com, or lksfy.com'
                }
                self.wfile.write(json.dumps(error_response).encode())
                return
            
            # Create session and call appropriate handler
            session = requests.Session()
            session.headers.update({"User-Agent": sigma_study_v4.DEFAULT_USER_AGENT})
            
            if 'nanolinks' in link:
                key, failed_url, error = sigma_study_v4.handle_nano_links(link, session, True, False)
            elif 'arolinks' in link:
                key, failed_url, error = sigma_study_v4.handle_aro_links(link, session, True, False)
            elif 'lksfy' in link:
                key, failed_url, error = sigma_study_v4.handle_lksfy(link, session, True, False)
            else:
                self.end_headers()
                error_response = {'success': False, 'error': 'Unsupported domain'}
                self.wfile.write(json.dumps(error_response).encode())
                return
            
            self.end_headers()
            if key:
                response = {'success': True, 'key': key}
                self.wfile.write(json.dumps(response).encode())
            else:
                error_response = {
                    'success': False,
                    'error': str(error) if error else 'Failed to extract key',
                    'failed_url': failed_url
                }
                self.wfile.write(json.dumps(error_response).encode())
                
        except Exception as e:
            self.end_headers()
            error_response = {'success': False, 'error': str(e)}
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
