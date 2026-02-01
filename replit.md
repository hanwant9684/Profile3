# Telegram Bot

## Overview

This is a Telegram bot built with Pyrogram that provides file transfer and management capabilities. It includes features like cloud backup, user authentication, admin controls, and file handling.

## Project Structure

- `main.py` - Entry point that initializes the bot and starts all services
- `bot/` - Core bot modules:
  - `config.py` - Configuration and Pyrogram client setup
  - `handlers.py` - Message and callback handlers
  - `login.py` - User login/session management
  - `admin.py` - Admin commands and controls
  - `database.py` - SQLite database operations
  - `cloud_backup.py` - Cloud backup/restore functionality
  - `transfer.py` - File transfer utilities
  - `web.py` - Optional Flask health check server
  - `ads.py` - Advertisement handling
  - `info.py` - Bot information commands
  - `logger.py` - Logging configuration
- `pyrogram/` - Custom/modified Pyrogram library

## Requirements

Python 3.12 with dependencies:
- pyrogram (custom version included)
- tgcrypto
- flask
- aiofiles, aiohttp
- uvloop
- psutil
- python-dotenv

## Environment Variables

Required:
- `API_ID` - Telegram API ID
- `API_HASH` - Telegram API Hash
- `BOT_TOKEN` - Telegram Bot Token

Optional:
- `OWNER_ID` - Bot owner's Telegram ID
- `OWNER_USERNAME` - Owner's username
- `DUMP_CHANNEL_ID` - Channel for file dumps
- `DATABASE_PATH` - SQLite database path (default: telegram_bot.db)
- `RUN_WEB_SERVER` - Set to "true" to enable health check server on port 5000
- Various payment/support links (PAYPAL_LINK, UPI_ID, etc.)

## Running the Bot

The bot runs via `python main.py` which:
1. Attempts to restore database from cloud backup
2. Initializes SQLite database
3. Starts cleanup and backup tasks
4. Optionally starts Flask health check server
5. Runs the Pyrogram bot client

## Database

Uses SQLite (file: telegram_bot.db) for storing user data, sessions, and bot state.
