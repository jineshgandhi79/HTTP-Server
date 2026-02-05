import os
import json
from utils import log, validate_path, generate_filename, rfc7231_date
from config import RESOURCE_DIR, UPLOAD_DIR

SUPPORTED_METHODS = ["GET", "POST"]

CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".txt": "application/octet-stream",
    ".png": "application/octet-stream",
    ".jpg": "application/octet-stream",
    ".jpeg": "application/octet-stream"
}

def parse_request(request_bytes: bytes) -> dict:
    try:
        request_text = request_bytes.decode("utf-8")
        lines = request_text.split("\r\n")
        request_line = lines[0].split()
        method, path, version = request_line
        headers = {}
        body_index = None
        for i, line in enumerate(lines[1:]):
            if line == "":
                body_index = i + 2
                break
            if ":" in line:
                k, v = line.split(":", 1)
                headers[k.strip()] = v.strip()
        body = "\r\n".join(lines[body_index:]) if body_index else ""
        return {
            "method": method,
            "path": path,
            "version": version,
            "headers": headers,
            "body": body
        }
    except Exception as e:
        log(f"Error parsing request: {e}")
        return None

def build_response(status_code: int, headers: dict = None, body: bytes = b"") -> bytes:
    reason = {
        200: "OK",
        201: "Created",
        400: "Bad Request",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        415: "Unsupported Media Type",
        500: "Internal Server Error",
        503: "Service Unavailable"
    }.get(status_code, "Unknown")
    response_line = f"HTTP/1.1 {status_code} {reason}\r\n"
    headers = headers or {}
    headers["Date"] = rfc7231_date()
    headers["Server"] = "Multi-threaded HTTP Server"
    header_lines = "".join(f"{k}: {v}\r\n" for k, v in headers.items())
    return (response_line + header_lines + "\r\n").encode() + body

def handle_get(request: dict) -> bytes:
    path = request["path"].lstrip("/")
    if path == "":
        path = "index.html"
    try:
        file_path = validate_path(path)
        if not os.path.exists(file_path):
            return build_response(404)
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in CONTENT_TYPES:
            return build_response(415)
        content_type = CONTENT_TYPES[ext]
        with open(file_path, "rb") as f:
            data = f.read()
        headers = {
            "Content-Type": content_type,
            "Content-Length": str(len(data)),
            "Connection": "close"
        }
        if content_type == "application/octet-stream":
            headers["Content-Disposition"] = f'attachment; filename="{os.path.basename(file_path)}"'
        return build_response(200, headers, data)
    except PermissionError:
        return build_response(403)
    except Exception:
        return build_response(500)

def handle_post(request: dict) -> bytes:
    if request["headers"].get("Content-Type") != "application/json":
        return build_response(415)
    try:
        data = json.loads(request["body"])
    except json.JSONDecodeError:
        return build_response(400)
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    filename = generate_filename()
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "w") as f:
        json.dump(data, f)
    response_body = json.dumps({
        "status": "success",
        "message": "File created successfully",
        "filepath": f"/uploads/{filename}"
    }).encode()
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(len(response_body)),
        "Connection": "close"
    }
    return build_response(201, headers, response_body)

def handle_request(request_bytes: bytes) -> bytes:
    request = parse_request(request_bytes)
    if not request:
        return build_response(400)
    method = request["method"]
    if method == "GET":
        return handle_get(request)
    elif method == "POST":
        return handle_post(request)
    else:
        return build_response(405)