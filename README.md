# Multi-threaded HTTP Server in Python

A fully functional **multi-threaded HTTP server** implemented from scratch in Python using **socket programming**. This server supports:

- Serving **HTML pages, text files, and images** (binary content)
- Handling **JSON POST requests** and saving uploads
- **Persistent connections** with keep-alive support
- **Thread pool** to handle concurrent clients efficiently
- Basic **security** features: path validation, host header check, and protection against path traversal

---

## 📁 Folder Structure

```
project/
├── server/
│   ├── server.py          # Main server entry point
│   ├── config.py          # Configuration settings
│   ├── utils.py           # Utility functions
│   ├── http_handler.py    # HTTP request handler
│   └── client.py          # Optional test client
├── resources/
│   ├── index.html         # Home page
│   ├── about.html         # About page
│   ├── contact.html       # Contact page
│   ├── sample.txt         # Sample text file
│   ├── logo.png           # Sample PNG image
│   ├── photo.jpg          # Sample JPEG image
│   └── uploads/           # Directory for POST uploads
└── README.md
```

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/jineshgandhi79/HTTP-Server
cd project
```

### 2. Create Virtual Environment (Optional but Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** This project primarily uses standard Python libraries. So no need to install requirements. It is empty as of now.

---

## 🖥️ Running the Server

Run the server using:

```bash
python server/server.py [port] [host] [max_threads]
```

### Parameters:
- **port**: Optional, default is `8080`
- **host**: Optional, default is `127.0.0.1`
- **max_threads**: Optional, default is `10`

### Example:

```bash
python server/server.py 8000 0.0.0.0 20
```

### Server Startup Log:

When the server starts, it will log the HTTP address in the terminal:

```
HTTP Server started on http://127.0.0.1:8080
Thread pool size: 10
Serving files from 'resources' directory
Press Ctrl+C to stop the server
```

Copy and paste the HTTP address into your browser to test the server.

---

## 🌐 Accessing HTML Pages (GET Requests)

Open a browser and navigate to:

- **Home page**: `http://127.0.0.1:8080/`
- **About page**: `http://127.0.0.1:8080/about.html`
- **Contact page**: `http://127.0.0.1:8080/contact.html`
- **Text file**: `http://127.0.0.1:8080/sample.txt`
- **PNG image**: `http://127.0.0.1:8080/logo.png`
- **JPEG image**: `http://127.0.0.1:8080/photo.jpg`

---

## 📤 POST Requests (JSON Uploads)

To upload JSON data, use `curl` (CMD/PowerShell) or tools like **Postman**.

### Using Windows CMD:

```cmd
curl -X POST http://127.0.0.1:8080/upload -H "Content-Type: application/json" -d "{\"name\": \"your_name\", \"age\": your_age}"
```


### Response:

Uploaded JSON files are stored in `resources/uploads/`. The server responds with:

```json
{
  "status": "success",
  "message": "File created successfully",
  "filepath": "/uploads/upload_<timestamp>_<random_id>.json"
}
```

---

## 🔒 Security Features

- **Path Traversal Protection**: All GET requests are validated to prevent directory traversal attacks
- **Host Header Validation**: Ensures requests are directed to the correct host
- **Content-Type Validation**: Only JSON `Content-Type` is accepted for POST requests
- **Invalid requests return appropriate HTTP status codes**:
  - `403 Forbidden` for path traversal attempts
  - `415 Unsupported Media Type` for invalid POST content types
  - `404 Not Found` for missing resources

---

## 📝 Notes

- Ensure the `resources/` folder contains `index.html` for the root path `/`
- All GET requests are validated for path traversal; invalid requests return `403 Forbidden`
- Only JSON `Content-Type` is accepted for POST requests; invalid requests return `415 Unsupported Media Type`
- The terminal log prints the exact HTTP address and port, which can