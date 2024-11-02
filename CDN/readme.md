# FastAPI CDN and Origin Servers

This project consists of two FastAPI servers:

1. `main.py` - Acts as the origin server, serving files from the `main` folder.
2. `cdn.py` - Acts as a CDN proxy server, caching requests and forwarding them to `main.py` when necessary.

## Setup

### Prerequisites

- Python 3.x
- FastAPI
- Uvicorn
- Requests library (for proxy functionality in `cdn.py`)

### Install Dependencies

To install the required packages, use:

```bash
pip install fastapi uvicorn requests
```

### Folder Structure

Ensure the folder structure is as follows:

```
project_folder/
├── cdn.py
├── main.py
├── main/            # Folder containing files to be served by main.py
│   └── example.txt  # Sample file
└── cdn/           # Folder where cdn.py will store cached responses
```

### Running the Servers

1. **Run `main.py`**: This server serves files from the `main` directory on port 8002.

   ```bash
   uvicorn main:app --reload --port 8002
   ```

2. **Run `cdn.py`**: This server runs the CDN proxy on port 8001.
   ```bash
   uvicorn cdn:app --reload --port 8001
   ```

## Usage

- To access a file (e.g., `example.txt`) via the origin server (`main.py`):

  ```
  http://localhost:8002/file/example.txt
  ```

- To access the same file via the CDN proxy (`cdn.py`), which will cache the response:
  ```
  http://localhost:8001/file/example.txt
  ```

## Explanation of Components

### main.py

- **Function**: Serves files from the `main` folder.
- **Endpoint**: `GET /{file_name}` - Retrieves a file if it exists in the `main` folder.

### cdn.py

- **Function**: Acts as a CDN proxy, caching requests and forwarding to `main.py` as needed.
- **Cache Behavior**: On receiving a request, `cdn.py` checks if the response is cached. If cached, it returns the cached response; otherwise, it forwards the request to `main.py`, caches the response, and then returns it to the client.

## Example

1. Place a file named `example.txt` in the `main` folder.
2. Access `example.txt` through the CDN server:
   ```
   http://localhost:8001/example.txt
   ```
3. The first request will be fetched from `main.py`, then cached by `cdn.py`. Subsequent requests will be served directly from the cache.

## Stopping the Servers

Press `CTRL+C` in the terminal where each server is running to stop them.

```

This README provides setup instructions, usage examples, and explanations in a clean, Markdown-friendly format.
```
