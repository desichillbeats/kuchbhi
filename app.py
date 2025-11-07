from flask import Flask, jsonify, request
import os
import sys
from sigma_study_v4 import (
    get_initial_response_headers,
    build_combined,
    decode_b64_xor,
    extract_baseurl,
    fetch_key_flow,
    DEFAULT_TARGET,
    DEFAULT_USER_AGENT,
    KEY,
    HEADER_NAMES
)

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'message': 'Sigma Study API',
        'endpoints': {
            '/api/get-key': 'GET - Extract key from target URL',
            '/api/health': 'GET - Health check'
        }
    })

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'sigma-study-api'})

@app.route('/api/get-key', methods=['GET'])
def get_key():
    try:
        # Get optional parameters
        target_url = request.args.get('target_url', DEFAULT_TARGET)
        ssl_bypass = request.args.get('ssl_bypass', 'false').lower() == 'true'
        debug = request.args.get('debug', 'false').lower() == 'true'
        
        verify = not ssl_bypass
        user_agent = DEFAULT_USER_AGENT
        
        # Suppress warnings if SSL bypass
        if ssl_bypass:
            try:
                import urllib3
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            except:
                pass
        
        # Get initial response
        headers, resp = get_initial_response_headers(target_url, user_agent, verify, debug)
        
        # Build combined payload
        combined, missing = build_combined(headers, debug)
        
        if all(not ch for ch in combined):
            return jsonify({
                'success': False,
                'error': 'Combined payload empty - server did not return required headers',
                'missing_headers': missing
            }), 400
        
        # Decode
        xor_key_bytes = KEY.encode('utf-8')
        decoded = decode_b64_xor(combined, xor_key_bytes, debug)
        
        # Extract baseUrl
        baseurl = extract_baseurl(decoded, debug)
        
        # Fetch key
        key, failed_url, error = fetch_key_flow(baseurl, verify=verify, debug=debug, user_agent=user_agent)
        
        if key:
            return jsonify({
                'success': True,
                'key': key,
                'baseUrl': baseurl
            })
        else:
            return jsonify({
                'success': False,
                'error': str(error) if error else 'Failed to extract key',
                'failed_url': failed_url
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)  
