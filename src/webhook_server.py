from flask import Flask, request
import sys

app = Flask(__name__)

# Very simple webhook to catch L3 exfiltrations for the demo
@app.route('/log', methods=['GET'])
def log_ping():
    print(f"\n🚨 PING RECEIVED! Query params: {request.args}", file=sys.stderr)
    return "OK", 200

if __name__ == '__main__':
    print("Starting Webhook Server on port 5000...")
    print("Wait for 'PING RECEIVED!' to appear here during the demo.")
    app.run(host='0.0.0.0', port=5000)
