# tests/test_web.py
# Basic web-app tests for the stdlib HTTP preview and API generation endpoints.
import json
import threading
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from ai_tc_gen.web import SAMPLE_SPEC, AITestCaseGeneratorHandler
from http.server import ThreadingHTTPServer


def start_test_server():
    server = ThreadingHTTPServer(('127.0.0.1', 0), AITestCaseGeneratorHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, f'http://127.0.0.1:{server.server_address[1]}'


def test_web_index_loads():
    server, base_url = start_test_server()
    try:
        with urlopen(f'{base_url}/') as response:
            body = response.read()

        assert response.status == 200
        assert b'AI Test Case Generator' in body
        assert b'Generate pytest test cases' in body
    finally:
        server.shutdown()


def test_web_generate_preview():
    server, base_url = start_test_server()
    try:
        data = urlencode({'spec': SAMPLE_SPEC, 'provider': 'local', 'action': 'preview'}).encode()
        request = Request(f'{base_url}/generate', data=data, method='POST')
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')

        with urlopen(request) as response:
            body = response.read()

        assert response.status == 200
        assert b'test_Create_Order_case_1' in body
        assert b'test_Create_Order_edge_2' in body
    finally:
        server.shutdown()


def test_web_api_generate():
    server, base_url = start_test_server()
    try:
        data = json.dumps({'spec': SAMPLE_SPEC, 'provider': 'local'}).encode()
        request = Request(f'{base_url}/api/generate', data=data, method='POST')
        request.add_header('Content-Type', 'application/json')

        with urlopen(request) as response:
            payload = json.loads(response.read().decode())

        assert response.status == 200
        assert 'test_Create_Order_case_1' in payload['output']
    finally:
        server.shutdown()
