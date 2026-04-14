#!/usr/bin/env python3
"""
Professional Multi-Purpose Python Tool with UI
Supports: Web Scraping, Automation, Data Analysis, API Interaction, File Manipulation, Encryption
"""

import sys
import os

# Check for required dependencies
missing_packages = []
required_packages = {
    'tkinter': 'tkinter (built-in, may need: sudo apt-get install python3-tk)',
    'requests': 'requests',
    'bs4': 'beautifulsoup4',
    'pandas': 'pandas',
}

print("Checking dependencies...")

try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, scrolledtext
except ImportError:
    print("ERROR: tkinter not found. Install with:")
    print("  Ubuntu/Debian: sudo apt-get install python3-tk")
    print("  macOS: brew install python-tk")
    print("  Windows: tkinter comes with Python")
    sys.exit(1)

try:
    import requests
except ImportError:
    missing_packages.append('requests')

try:
    from bs4 import BeautifulSoup
except ImportError:
    missing_packages.append('beautifulsoup4')

try:
    import pandas as pd
except ImportError:
    missing_packages.append('pandas')

# Optional encryption libraries
try:
    from cryptography.fernet import Fernet, InvalidToken
    FERNET_AVAILABLE = True
except ImportError:
    FERNET_AVAILABLE = False
    print("⚠️  Warning: cryptography not installed. Fernet encryption disabled.")
    print("   Install with: pip install cryptography")

try:
    import jwt
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False
    print("⚠️  Warning: PyJWT not installed. JWT encoding disabled.")
    print("   Install with: pip install PyJWT")

if missing_packages:
    print(f"\n❌ ERROR: Missing packages: {', '.join(missing_packages)}")
    print("\nInstall them with:")
    print(f"  pip install {' '.join(missing_packages)}")
    sys.exit(1)

print("✅ All dependencies OK!\n")

import threading
import json
import csv
import sqlite3
from datetime import datetime
from urllib.parse import quote, unquote
import re
from pathlib import Path
import base64
import hmac
import hashlib


class ToolConfig:
    """Configuration and settings"""
    WINDOW_WIDTH = 1400
    WINDOW_HEIGHT = 900
    BG_COLOR = "#1e1e1e"
    FG_COLOR = "#ffffff"
    ACCENT_COLOR = "#0078d4"
    SUCCESS_COLOR = "#07a62b"
    ERROR_COLOR = "#f44747"
    WARNING_COLOR = "#dcdcaa"


class OutputLogger:
    """Capture and display output"""
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def log(self, message, level="INFO"):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.text_widget.config(state=tk.NORMAL)
        
        if level == "ERROR":
            self.text_widget.insert(tk.END, f"[{timestamp}] ❌ {message}\n", "error")
        elif level == "SUCCESS":
            self.text_widget.insert(tk.END, f"[{timestamp}] ✅ {message}\n", "success")
        elif level == "WARNING":
            self.text_widget.insert(tk.END, f"[{timestamp}] ⚠️  {message}\n", "warning")
        else:
            self.text_widget.insert(tk.END, f"[{timestamp}] ℹ️  {message}\n", "info")
        
        self.text_widget.see(tk.END)
        self.text_widget.config(state=tk.DISABLED)
        self.text_widget.update()

    def clear(self):
        """Clear output"""
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.config(state=tk.DISABLED)


class WebScraperModule:
    """Web scraping functionality"""
    
    @staticmethod
    def scrape_url(url, logger):
        """Scrape website and extract data"""
        try:
            logger.log(f"Fetching: {url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            logger.log(f"Status Code: {response.status_code}", "SUCCESS")
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title = soup.find('title')
            headings = soup.find_all(['h1', 'h2', 'h3'])
            links = soup.find_all('a')
            images = soup.find_all('img')
            paragraphs = soup.find_all('p')
            
            data = {
                'title': title.text if title else 'No title found',
                'url': url,
                'headings': [h.text.strip() for h in headings[:5]],
                'links_count': len(links),
                'images_count': len(images),
                'paragraphs_count': len(paragraphs),
                'links': [{'text': a.text.strip(), 'href': a.get('href')} for a in links[:10]],
                'images': [img.get('src') for img in images[:5]]
            }
            
            return data
        
        except Exception as e:
            raise Exception(f"Scraping error: {str(e)}")


class DataAnalysisModule:
    """Data analysis and processing"""
    
    @staticmethod
    def load_csv(filepath, logger):
        """Load and analyze CSV file"""
        try:
            df = pd.read_csv(filepath)
            logger.log(f"Loaded CSV with {len(df)} rows and {len(df.columns)} columns", "SUCCESS")
            
            stats = {
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': df.columns.tolist(),
            }
            
            return df, stats
        
        except Exception as e:
            raise Exception(f"CSV loading error: {str(e)}")
    
    @staticmethod
    def analyze_text(text, logger):
        """Analyze text statistics"""
        try:
            words = text.split()
            lines = text.split('\n')
            
            stats = {
                'total_characters': len(text),
                'total_words': len(words),
                'total_lines': len(lines),
                'avg_word_length': sum(len(w) for w in words) / len(words) if words else 0,
                'unique_words': len(set(w.lower() for w in words)),
                'sentences': len(re.split(r'[.!?]+', text)),
                'numbers': len(re.findall(r'\d+', text)),
                'special_chars': len(re.findall(r'[^a-zA-Z0-9\s]', text))
            }
            
            logger.log("Text analysis completed", "SUCCESS")
            return stats
        
        except Exception as e:
            raise Exception(f"Text analysis error: {str(e)}")


class APIModule:
    """API interaction and testing"""
    
    @staticmethod
    def make_request(method, url, headers_str, body_str, logger):
        """Make HTTP request"""
        try:
            logger.log(f"Making {method} request to: {url}")
            
            headers = {}
            if headers_str.strip():
                try:
                    headers = json.loads(headers_str)
                except json.JSONDecodeError:
                    raise Exception("Invalid JSON in headers")
            
            data = None
            if body_str.strip():
                try:
                    data = json.loads(body_str)
                except json.JSONDecodeError:
                    raise Exception("Invalid JSON in body")
            
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=data, timeout=10)
            elif method == "PUT":
                response = requests.put(url, headers=headers, json=data, timeout=10)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, timeout=10)
            elif method == "PATCH":
                response = requests.patch(url, headers=headers, json=data, timeout=10)
            else:
                raise Exception("Unsupported HTTP method")
            
            logger.log(f"Response Status: {response.status_code}", "SUCCESS")
            
            try:
                response_data = response.json()
            except:
                response_data = response.text
            
            result = {
                'status_code': response.status_code,
                'body': response_data,
                'time': response.elapsed.total_seconds()
            }
            
            return result
        
        except Exception as e:
            raise Exception(f"API request error: {str(e)}")


class FileModule:
    """File manipulation and conversion"""
    
    @staticmethod
    def convert_json_to_csv(json_file, csv_file, logger):
        """Convert JSON to CSV"""
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                df = pd.DataFrame(data)
            else:
                df = pd.DataFrame([data])
            
            df.to_csv(csv_file, index=False)
            logger.log(f"Converted to CSV: {csv_file}", "SUCCESS")
            return True
        
        except Exception as e:
            raise Exception(f"Conversion error: {str(e)}")
    
    @staticmethod
    def convert_csv_to_json(csv_file, json_file, logger):
        """Convert CSV to JSON"""
        try:
            df = pd.read_csv(csv_file)
            df.to_json(json_file, orient='records', indent=2)
            logger.log(f"Converted to JSON: {json_file}", "SUCCESS")
            return True
        
        except Exception as e:
            raise Exception(f"Conversion error: {str(e)}")
    
    @staticmethod
    def merge_files(files, output_file, logger):
        """Merge multiple files"""
        try:
            dfs = []
            for file in files:
                if file.endswith('.csv'):
                    df = pd.read_csv(file)
                elif file.endswith('.json'):
                    df = pd.read_json(file)
                else:
                    raise Exception(f"Unsupported format: {file}")
                dfs.append(df)
            
            merged = pd.concat(dfs, ignore_index=True)
            
            if output_file.endswith('.csv'):
                merged.to_csv(output_file, index=False)
            elif output_file.endswith('.json'):
                merged.to_json(output_file, orient='records', indent=2)
            
            logger.log(f"Merged {len(files)} files into: {output_file}", "SUCCESS")
            return True
        
        except Exception as e:
            raise Exception(f"Merge error: {str(e)}")


class EncryptionModule:
    """Comprehensive encryption and decryption module"""
    
    # Base64
    @staticmethod
    def encode_base64(data: str):
        """Encode Base64"""
        try:
            return base64.b64encode(data.encode()).decode()
        except Exception as e:
            raise Exception(f"Base64 encode error: {str(e)}")
    
    @staticmethod
    def decode_base64(data: str):
        """Decode Base64"""
        try:
            # Add padding if needed
            missing_padding = len(data) % 4
            if missing_padding:
                data += '=' * (4 - missing_padding)
            return base64.b64decode(data).decode('utf-8')
        except Exception as e:
            raise Exception(f"Base64 decode error: {str(e)}")
    
    # URL-Safe Base64
    @staticmethod
    def encode_urlsafe_base64(data: str):
        """Encode URL-safe Base64"""
        try:
            return base64.urlsafe_b64encode(data.encode()).decode().rstrip('=')
        except Exception as e:
            raise Exception(f"URL-safe Base64 encode error: {str(e)}")
    
    @staticmethod
    def decode_urlsafe_base64(data: str):
        """Decode URL-safe Base64"""
        try:
            # Add padding if needed
            missing_padding = len(data) % 4
            if missing_padding:
                data += '=' * (4 - missing_padding)
            return base64.urlsafe_b64decode(data).decode('utf-8')
        except Exception as e:
            raise Exception(f"URL-safe Base64 decode error: {str(e)}")
    
    # Hexadecimal
    @staticmethod
    def encode_hex(data: str):
        """Encode to Hexadecimal"""
        try:
            return data.encode().hex()
        except Exception as e:
            raise Exception(f"Hex encode error: {str(e)}")
    
    @staticmethod
    def decode_hex(data: str):
        """Decode Hexadecimal"""
        try:
            return bytes.fromhex(data).decode('utf-8')
        except Exception as e:
            raise Exception(f"Hex decode error: {str(e)}")
    
    # ROT13
    @staticmethod
    def encode_rot13(data: str):
        """Encode ROT13"""
        result = []
        for char in data:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result.append(chr((ord(char) - base + 13) % 26 + base))
            else:
                result.append(char)
        return ''.join(result)
    
    @staticmethod
    def decode_rot13(data: str):
        """Decode ROT13 (same as encode)"""
        return EncryptionModule.encode_rot13(data)
    
    # Caesar Cipher
    @staticmethod
    def encode_caesar(data: str, shift: int = 3):
        """Encode Caesar cipher"""
        result = []
        for char in data:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result.append(chr((ord(char) - base + shift) % 26 + base))
            else:
                result.append(char)
        return ''.join(result)
    
    @staticmethod
    def decode_caesar(data: str, shift: int = 3):
        """Decode Caesar cipher"""
        result = []
        for char in data:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result.append(chr((ord(char) - base - shift) % 26 + base))
            else:
                result.append(char)
        return ''.join(result)
    
    # HMAC
    @staticmethod
    def generate_hmac(data: str, secret: str, algorithm: str = "sha256"):
        """Generate HMAC signature"""
        try:
            hash_obj = hmac.new(secret.encode(), data.encode(), getattr(hashlib, algorithm))
            return hash_obj.hexdigest()
        except Exception as e:
            raise Exception(f"HMAC error: {str(e)}")
    
    # URL Encoding
    @staticmethod
    def encode_url(data: str):
        """Encode URL"""
        try:
            return quote(data)
        except Exception as e:
            raise Exception(f"URL encode error: {str(e)}")
    
    @staticmethod
    def decode_url(data: str):
        """Decode URL"""
        try:
            return unquote(data)
        except Exception as e:
            raise Exception(f"URL decode error: {str(e)}")
    
    # JWT
    @staticmethod
    def encode_jwt(payload: dict, secret: str = "your-secret-key", algorithm: str = "HS256"):
        """Encode JWT"""
        if not JWT_AVAILABLE:
            raise Exception("PyJWT not installed. Install with: pip install PyJWT")
        
        try:
            # Ensure payload is a dict
            if not isinstance(payload, dict):
                payload = {"data": str(payload)}
            
            if "iat" not in payload:
                payload["iat"] = int(datetime.utcnow().timestamp())
            token = jwt.encode(payload, secret, algorithm=algorithm)
            return token
        except Exception as e:
            raise Exception(f"JWT encode error: {str(e)}")
    
    @staticmethod
    def decode_jwt(token: str, secret: str = None, verify: bool = False):
        """Decode JWT"""
        if not JWT_AVAILABLE:
            # Manual JWT decoding without verification
            try:
                parts = token.split('.')
                if len(parts) != 3:
                    raise ValueError("Invalid JWT format (must have 3 parts)")
                
                # Decode header and payload (they're base64)
                header_data = EncryptionModule.decode_base64(parts[0])
                payload_data = EncryptionModule.decode_base64(parts[1])
                
                return {
                    "status": "decoded (unverified - PyJWT not installed)",
                    "header": json.loads(header_data),
                    "payload": json.loads(payload_data),
                    "signature": parts[2]
                }
            except Exception as e:
                raise Exception(f"JWT decode error: {str(e)}")
        
        try:
            if verify and secret:
                decoded = jwt.decode(token, secret, algorithms=["HS256", "HS512", "RS256"])
                return {"status": "verified", "payload": decoded}
            else:
                decoded = jwt.decode(token, options={"verify_signature": False})
                return {"status": "decoded (unverified)", "payload": decoded}
        except Exception as e:
            raise Exception(f"JWT decode error: {str(e)}")
    
    # Fernet
    @staticmethod
    def encode_fernet(payload, key: str = None):
        """Encode Fernet"""
        if not FERNET_AVAILABLE:
            raise Exception("cryptography not installed. Install with: pip install cryptography")
        
        try:
            if isinstance(payload, dict):
                data = json.dumps(payload)
            else:
                data = str(payload)
            
            if not key:
                key = Fernet.generate_key().decode()
            
            # Handle both string and bytes keys
            try:
                if isinstance(key, str):
                    key_bytes = key.encode() if len(key) == 44 else Fernet.generate_key()
                else:
                    key_bytes = key
                cipher = Fernet(key_bytes)
            except:
                # If key is invalid, generate new one
                key_bytes = Fernet.generate_key()
                key = key_bytes.decode()
                cipher = Fernet(key_bytes)
            
            encrypted = cipher.encrypt(data.encode())
            
            return {
                "token": encrypted.decode(),
                "key": key if isinstance(key, str) else key.decode()
            }
        except Exception as e:
            raise Exception(f"Fernet encode error: {str(e)}")
    
    @staticmethod
    def decode_fernet(token: str, key: str = None):
        """Decode Fernet"""
        if not FERNET_AVAILABLE:
            raise Exception("cryptography not installed. Install with: pip install cryptography")
        
        try:
            if not key or key.strip() == "":
                raise ValueError("Fernet key is required for decryption (save the key from encryption)")
            
            # Handle both string and bytes keys
            try:
                if isinstance(key, str):
                    key_bytes = key.encode()
                else:
                    key_bytes = key
                cipher = Fernet(key_bytes)
            except Exception as ke:
                raise ValueError(f"Invalid Fernet key format: {str(ke)}")
            
            decrypted = cipher.decrypt(token.encode())
            
            try:
                return {
                    "status": "decrypted",
                    "data": json.loads(decrypted.decode())
                }
            except:
                return {
                    "status": "decrypted",
                    "data": decrypted.decode()
                }
        except Exception as e:
            raise Exception(f"Fernet decode error: {str(e)}")


class MainApp(tk.Tk):
    """Main Application Window"""
    
    def __init__(self):
        super().__init__()
        self.title("🛠️  Web Tools")
        self.geometry(f"{ToolConfig.WINDOW_WIDTH}x{ToolConfig.WINDOW_HEIGHT}")
        self.configure(bg=ToolConfig.BG_COLOR)
        self.style_setup()
        
        self.create_widgets()
        
    def style_setup(self):
        """Setup custom styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TFrame', background=ToolConfig.BG_COLOR)
        style.configure('TLabel', background=ToolConfig.BG_COLOR, foreground=ToolConfig.FG_COLOR)
        style.configure('TNotebook', background=ToolConfig.BG_COLOR)
        
    def create_widgets(self):
        """Create main UI"""
        header = ttk.Frame(self)
        header.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = ttk.Label(header, text="🛠️  Professional Python Tool Suite", 
                               font=("Arial", 18, "bold"))
        title_label.pack(side=tk.LEFT)
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.create_web_scraper_tab()
        self.create_data_analysis_tab()
        self.create_api_tester_tab()
        self.create_file_converter_tab()
        self.create_encryption_tab()
        
        output_frame = ttk.LabelFrame(self, text="📊 Output & Logs", padding=10)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=8, 
                                                      bg="#2d2d2d", fg=ToolConfig.FG_COLOR,
                                                      font=("Courier", 9))
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        self.output_text.tag_config("error", foreground=ToolConfig.ERROR_COLOR)
        self.output_text.tag_config("success", foreground=ToolConfig.SUCCESS_COLOR)
        self.output_text.tag_config("warning", foreground=ToolConfig.WARNING_COLOR)
        self.output_text.tag_config("info", foreground="#569cd6")
        
        self.logger = OutputLogger(self.output_text)
        self.logger.log("Application started successfully!", "SUCCESS")
        
        clear_btn = ttk.Button(output_frame, text="Clear Output", command=self.logger.clear)
        clear_btn.pack(side=tk.LEFT, padx=5, pady=5)
    
    def create_web_scraper_tab(self):
        """Web Scraper Tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🌐 Web Scraper")
        
        ttk.Label(frame, text="URL:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        url_entry = ttk.Entry(frame, width=60)
        url_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        url_entry.insert(0, "https://example.com")
        
        def scrape():
            def task():
                try:
                    url = url_entry.get()
                    if not url.startswith('http'):
                        url = 'https://' + url
                    
                    data = WebScraperModule.scrape_url(url, self.logger)
                    self.logger.log("\n=== SCRAPING RESULTS ===", "INFO")
                    self.logger.log(f"Title: {data['title']}", "INFO")
                    self.logger.log(f"Links found: {data['links_count']}", "SUCCESS")
                
                except Exception as e:
                    self.logger.log(str(e), "ERROR")
            
            thread = threading.Thread(target=task, daemon=True)
            thread.start()
        
        ttk.Button(frame, text="Scrape Website", command=scrape).grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        frame.columnconfigure(1, weight=1)
    
    def create_data_analysis_tab(self):
        """Data Analysis Tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📈 Data Analysis")
        
        csv_frame = ttk.LabelFrame(frame, text="CSV Analysis")
        csv_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def analyze_csv():
            file = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
            if file:
                try:
                    df, stats = DataAnalysisModule.load_csv(file, self.logger)
                    self.logger.log("\n=== CSV STATISTICS ===", "INFO")
                    self.logger.log(f"Rows: {stats['rows']}, Columns: {stats['columns']}", "INFO")
                    self.logger.log(f"Columns: {', '.join(stats['column_names'])}", "INFO")
                except Exception as e:
                    self.logger.log(str(e), "ERROR")
        
        ttk.Button(csv_frame, text="Analyze CSV", command=analyze_csv).pack(padx=10, pady=10)
        
        text_frame = ttk.LabelFrame(frame, text="Text Analysis")
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_input = tk.Text(text_frame, height=10, bg="#2d2d2d", 
                            fg=ToolConfig.FG_COLOR, font=("Courier", 9))
        text_input.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        def analyze_text():
            text = text_input.get(1.0, tk.END)
            if text.strip():
                try:
                    stats = DataAnalysisModule.analyze_text(text, self.logger)
                    self.logger.log("\n=== TEXT STATISTICS ===", "INFO")
                    for key, value in stats.items():
                        self.logger.log(f"{key}: {value}", "INFO")
                except Exception as e:
                    self.logger.log(str(e), "ERROR")
        
        ttk.Button(text_frame, text="Analyze Text", command=analyze_text).pack(padx=10, pady=5)
    
    def create_api_tester_tab(self):
        """API Tester Tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔌 API Tester")
        
        ttk.Label(frame, text="Method:").grid(row=0, column=0, padx=10, pady=10)
        method_var = tk.StringVar(value="GET")
        method_combo = ttk.Combobox(frame, textvariable=method_var, 
                                    values=["GET", "POST", "PUT", "DELETE", "PATCH"],
                                    state="readonly", width=10)
        method_combo.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        ttk.Label(frame, text="URL:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        url_entry = ttk.Entry(frame, width=60)
        url_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        url_entry.insert(0, "https://api.example.com/endpoint")
        
        ttk.Label(frame, text="Headers (JSON):").grid(row=2, column=0, padx=10, pady=10, sticky="nw")
        headers_text = tk.Text(frame, height=4, width=60, bg="#2d2d2d", 
                              fg=ToolConfig.FG_COLOR, font=("Courier", 9))
        headers_text.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        headers_text.insert(1.0, '{"Content-Type": "application/json"}')
        
        ttk.Label(frame, text="Body (JSON):").grid(row=3, column=0, padx=10, pady=10, sticky="nw")
        body_text = tk.Text(frame, height=6, width=60, bg="#2d2d2d", 
                           fg=ToolConfig.FG_COLOR, font=("Courier", 9))
        body_text.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
        body_text.insert(1.0, '{"key": "value"}')
        
        def make_request():
            def task():
                try:
                    result = APIModule.make_request(method_var.get(), url_entry.get(),
                                                    headers_text.get(1.0, tk.END),
                                                    body_text.get(1.0, tk.END),
                                                    self.logger)
                    self.logger.log("\n=== API RESPONSE ===", "INFO")
                    self.logger.log(f"Status: {result['status_code']}", "SUCCESS")
                    self.logger.log(f"Response:\n{json.dumps(result['body'], indent=2)}", "INFO")
                except Exception as e:
                    self.logger.log(str(e), "ERROR")
            
            thread = threading.Thread(target=task, daemon=True)
            thread.start()
        
        ttk.Button(frame, text="Send Request", command=make_request).grid(row=4, column=0, 
                                                                           columnspan=2, padx=10, pady=10)
        frame.columnconfigure(1, weight=1)
    
    def create_file_converter_tab(self):
        """File Converter Tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📁 File Converter")
        
        ttk.Label(frame, text="Conversion Type:").grid(row=0, column=0, padx=10, pady=10)
        conv_var = tk.StringVar(value="JSON to CSV")
        conv_combo = ttk.Combobox(frame, textvariable=conv_var,
                                 values=["JSON to CSV", "CSV to JSON", "Merge Files"],
                                 state="readonly", width=20)
        conv_combo.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        def select_files():
            conv_type = conv_var.get()
            
            if conv_type == "JSON to CSV":
                input_file = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
                if input_file:
                    output_file = filedialog.asksaveasfilename(defaultextension=".csv",
                                                              filetypes=[("CSV", "*.csv")])
                    if output_file:
                        try:
                            FileModule.convert_json_to_csv(input_file, output_file, self.logger)
                        except Exception as e:
                            self.logger.log(str(e), "ERROR")
            
            elif conv_type == "CSV to JSON":
                input_file = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
                if input_file:
                    output_file = filedialog.asksaveasfilename(defaultextension=".json",
                                                              filetypes=[("JSON", "*.json")])
                    if output_file:
                        try:
                            FileModule.convert_csv_to_json(input_file, output_file, self.logger)
                        except Exception as e:
                            self.logger.log(str(e), "ERROR")
            
            elif conv_type == "Merge Files":
                files = filedialog.askopenfilenames(filetypes=[("CSV/JSON", "*.csv;*.json")])
                if files:
                    output_file = filedialog.asksaveasfilename(defaultextension=".csv",
                                                              filetypes=[("CSV", "*.csv"), 
                                                                        ("JSON", "*.json")])
                    if output_file:
                        try:
                            FileModule.merge_files(list(files), output_file, self.logger)
                        except Exception as e:
                            self.logger.log(str(e), "ERROR")
        
        ttk.Button(frame, text="Start Conversion", command=select_files).grid(row=1, column=0,
                                                                               columnspan=2, padx=10, pady=10)
    
    def create_encryption_tab(self):
        """Encryption/Decryption Tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔐 Encrypt/Decrypt")
        
        # Left panel - controls
        control_frame = ttk.LabelFrame(frame, text="⚙️  Settings", padding=10)
        control_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)
        
        # Right panel - input/output
        content_frame = ttk.LabelFrame(frame, text="📝 Data", padding=10)
        content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Encryption type selection
        ttk.Label(control_frame, text="Encryption Type:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        enc_var = tk.StringVar(value="Base64")
        enc_types = ["Base64", "URL-Safe Base64", "Hexadecimal", "JWT", "Fernet", 
                     "ROT13", "Caesar Cipher", "HMAC", "URL Encoding"]
        
        for enc_type in enc_types:
            ttk.Radiobutton(control_frame, text=enc_type, variable=enc_var, 
                          value=enc_type).pack(anchor=tk.W, padx=20)
        
        ttk.Separator(control_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=15)
        
        # Secret key input
        ttk.Label(control_frame, text="Secret/Key:", font=("Arial", 9, "bold")).pack(anchor=tk.W, pady=(10, 5))
        secret_entry = ttk.Entry(control_frame, width=25)
        secret_entry.pack(anchor=tk.W, padx=10, pady=5)
        secret_entry.insert(0, "your-secret-key")
        
        # Algorithm selection
        ttk.Label(control_frame, text="Algorithm:", font=("Arial", 9, "bold")).pack(anchor=tk.W, pady=(10, 5))
        algo_var = tk.StringVar(value="sha256")
        algo_combo = ttk.Combobox(control_frame, textvariable=algo_var, state="readonly", width=22,
                                 values=["sha256", "sha512", "md5", "HS256", "HS512"])
        algo_combo.pack(anchor=tk.W, padx=10, pady=5)
        
        # Caesar shift
        ttk.Label(control_frame, text="Caesar Shift:", font=("Arial", 9, "bold")).pack(anchor=tk.W, pady=(10, 5))
        shift_var = tk.StringVar(value="3")
        shift_entry = ttk.Entry(control_frame, textvariable=shift_var, width=25)
        shift_entry.pack(anchor=tk.W, padx=10, pady=5)
        
        ttk.Separator(control_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=15)
        
        # Input/Output areas
        ttk.Label(content_frame, text="Input Data:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        input_text = tk.Text(content_frame, height=10, bg="#2d2d2d", 
                            fg=ToolConfig.FG_COLOR, font=("Courier", 9))
        input_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        ttk.Label(content_frame, text="Output Data:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 0))
        output_text = tk.Text(content_frame, height=10, bg="#2d2d2d", 
                             fg=ToolConfig.FG_COLOR, font=("Courier", 9))
        output_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        def encrypt_action():
            try:
                enc_type = enc_var.get()
                data = input_text.get(1.0, tk.END).strip()
                secret = secret_entry.get()
                algo = algo_var.get()
                
                if not data:
                    self.logger.log("Please enter data to encrypt", "WARNING")
                    return
                
                try:
                    shift = int(shift_var.get())
                except:
                    shift = 3
                
                output_text.config(state=tk.NORMAL)
                output_text.delete(1.0, tk.END)
                
                result = None
                extra_output = None
                
                if enc_type == "Base64":
                    result = EncryptionModule.encode_base64(data)
                elif enc_type == "URL-Safe Base64":
                    result = EncryptionModule.encode_urlsafe_base64(data)
                elif enc_type == "Hexadecimal":
                    result = EncryptionModule.encode_hex(data)
                elif enc_type == "URL Encoding":
                    result = EncryptionModule.encode_url(data)
                elif enc_type == "ROT13":
                    result = EncryptionModule.encode_rot13(data)
                elif enc_type == "Caesar Cipher":
                    result = EncryptionModule.encode_caesar(data, shift)
                elif enc_type == "HMAC":
                    result = EncryptionModule.generate_hmac(data, secret, algo)
                elif enc_type == "JWT":
                    try:
                        payload = json.loads(data)
                    except:
                        payload = {"data": data}
                    result = EncryptionModule.encode_jwt(payload, secret, algo)
                elif enc_type == "Fernet":
                    res = EncryptionModule.encode_fernet(data, secret if secret != "your-secret-key" else None)
                    extra_output = f"TOKEN:\n{res['token']}\n\nKEY (SAVE THIS!):\n{res['key']}"
                
                if extra_output:
                    output_text.insert(tk.END, extra_output)
                elif result:
                    output_text.insert(tk.END, result)
                
                output_text.config(state=tk.DISABLED)
                self.logger.log(f"{enc_type} encrypted successfully", "SUCCESS")
            
            except Exception as e:
                output_text.config(state=tk.NORMAL)
                output_text.delete(1.0, tk.END)
                output_text.insert(tk.END, f"Error: {str(e)}")
                output_text.config(state=tk.DISABLED)
                self.logger.log(str(e), "ERROR")
        
        def decrypt_action():
            try:
                enc_type = enc_var.get()
                data = input_text.get(1.0, tk.END).strip()
                secret = secret_entry.get()
                algo = algo_var.get()
                
                if not data:
                    self.logger.log("Please enter data to decrypt", "WARNING")
                    return
                
                try:
                    shift = int(shift_var.get())
                except:
                    shift = 3
                
                output_text.config(state=tk.NORMAL)
                output_text.delete(1.0, tk.END)
                
                result = None
                extra_output = None
                
                if enc_type == "Base64":
                    result = EncryptionModule.decode_base64(data)
                elif enc_type == "URL-Safe Base64":
                    result = EncryptionModule.decode_urlsafe_base64(data)
                elif enc_type == "Hexadecimal":
                    result = EncryptionModule.decode_hex(data)
                elif enc_type == "URL Encoding":
                    result = EncryptionModule.decode_url(data)
                elif enc_type == "ROT13":
                    result = EncryptionModule.decode_rot13(data)
                elif enc_type == "Caesar Cipher":
                    result = EncryptionModule.decode_caesar(data, shift)
                elif enc_type == "HMAC":
                    self.logger.log("HMAC cannot be decrypted (it's one-way)", "WARNING")
                    output_text.config(state=tk.DISABLED)
                    return
                elif enc_type == "JWT":
                    res = EncryptionModule.decode_jwt(data, secret, False)
                    extra_output = json.dumps(res, indent=2)
                elif enc_type == "Fernet":
                    res = EncryptionModule.decode_fernet(data, secret)
                    extra_output = json.dumps(res, indent=2)
                
                if extra_output:
                    output_text.insert(tk.END, extra_output)
                elif result:
                    output_text.insert(tk.END, result)
                
                output_text.config(state=tk.DISABLED)
                self.logger.log(f"{enc_type} decrypted successfully", "SUCCESS")
            
            except Exception as e:
                output_text.config(state=tk.NORMAL)
                output_text.delete(1.0, tk.END)
                output_text.insert(tk.END, f"Error: {str(e)}")
                output_text.config(state=tk.DISABLED)
                self.logger.log(str(e), "ERROR")
        
        def copy_output():
            output = output_text.get(1.0, tk.END).strip()
            if output:
                input_text.delete(1.0, tk.END)
                input_text.insert(tk.END, output)
        
        ttk.Button(button_frame, text="🔒 Encrypt", command=encrypt_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔓 Decrypt", command=decrypt_action).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📋 Copy Output", command=copy_output).pack(side=tk.LEFT, padx=5)


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()