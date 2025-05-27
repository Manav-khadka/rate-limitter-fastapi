# FastAPI Rate Limiter

A simple FastAPI app with rate limiting to control the number of requests a client can make.

## Features

- Per-client rate limiting
- Custom limit and time window
- Middleware-based for easy integration

## Requirements

- `fastapi`
- `uvicorn`
- `slowapi` (or implement your own logic)

## Installation

```bash
pip install fastapi uvicorn slowapi
