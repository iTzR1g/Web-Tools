# Web-Tools
(notice : the tool is vibecoded)
#Setup & Usage Guide

## 📋 Features

Your custom Python tool includes:

### 1. **Web Scraper** 🌐
- Fetch and parse websites
- Extract titles, headings, links, images
- Save scraped data as JSON
- User-Agent headers for compatibility

### 2. **Data Analysis** 📈
- **CSV Analysis**: Load, analyze statistics, identify missing values
- **Text Analysis**: Character count, word count, unique words, sentence analysis
- Advanced statistical breakdowns

### 3. **API Tester** 🔌
- Test REST APIs (GET, POST, PUT, DELETE, PATCH)
- Custom headers and JSON body support
- Response time tracking
- Detailed response inspection

### 4. **File Converter** 📁
- JSON ↔ CSV conversion
- Merge multiple files
- Batch processing support

---

## 🚀 Installation

### Step 1: Install Python (3.8+)
Download from: https://www.python.org/

### Step 2: Install Required Libraries
```bash
pip install requests beautifulsoup4 pandas
```

### Step 3: Run the Tool
```bash
python my_python_tool.py
```

---

## 🎨 UI Overview

The tool has a modern dark-themed interface with:
- **Tabbed Navigation** - Switch between different tools
- **Real-time Logging** - Color-coded output (Success, Error, Warning, Info)
- **File Dialogs** - Easy file selection
- **Threading** - Non-blocking operations

---

## 💡 Usage Examples

### Web Scraper Tab
1. Enter URL (e.g., `https://example.com`)
2. Click "Scrape Website"
3. Choose location to save JSON results
4. View results in the output panel

**Example Output:**
```json
{
  "title": "Example Domain",
  "url": "https://example.com",
  "headings": ["Example Domain"],
  "links_count": 1,
  "images_count": 0,
  "links": [{"text": "More information...", "href": "https://www.iana.org/..."}]
}
```

### Data Analysis Tab
#### CSV Analysis
1. Click "Analyze CSV"
2. Select your CSV file
3. View statistics in output panel

**Shows:**
- Row and column count
- Column names and data types
- Missing values
- Numeric statistics

#### Text Analysis
1. Paste text in the input area
2. Click "Analyze Text"
3. View detailed statistics

**Shows:**
- Character/word/line counts
- Average word length
- Unique word count
- Sentence count
- Number of special characters

### API Tester Tab
1. Select HTTP method (GET, POST, PUT, DELETE, PATCH)
2. Enter API URL
3. Add headers (JSON format) - optional
4. Add request body (JSON format) - optional for POST/PUT
5. Click "Send Request"
6. View response status, time, and body

**Example Request:**
```
Method: POST
URL: https://api.example.com/users
Headers: {"Authorization": "Bearer token123", "Content-Type": "application/json"}
Body: {"name": "John", "email": "john@example.com"}
```

### File Converter Tab
1. Select conversion type:
   - **JSON to CSV** - Convert single JSON file
   - **CSV to JSON** - Convert single CSV file
   - **Merge Files** - Combine multiple CSV/JSON files
2. Select input file(s)
3. Choose output location
4. Click "Start Conversion"

**Merge Example:**
- Combine: `data1.csv`, `data2.csv`, `data3.csv`
- Output: `merged.csv` (all data combined)

---

## 🔧 Customization

### Modify the Tool
Edit `my_python_tool.py` to add your own features:

```python
# Example: Add new module
class MyCustomModule:
    @staticmethod
    def my_function(data):
        # Your code here
        return result
```

### Add New Tab
```python
def create_custom_tab(self):
    frame = ttk.Frame(self.notebook)
    self.notebook.add(frame, text="📌 My Custom Tab")
    
    # Add your widgets
    ttk.Label(frame, text="Hello!").pack()
```

---

## 📊 Output Log Colors

- 🟢 **Green (✅)** - Success messages
- 🔴 **Red (❌)** - Error messages
- 🟡 **Yellow (⚠️)** - Warning messages
- 🔵 **Blue (ℹ️)** - Info messages

Use "Clear Output" button to reset logs.

---

## ⚠️ Important Notes

### Security
- API keys and tokens: Use environment variables, not hardcoded
- Web scraping: Check website's robots.txt and terms of service
- User-Agent: Always include proper headers when scraping

### Performance
- Large files may take time to process
- The tool uses threading to prevent UI freezing
- Output is limited to last 1000 lines for performance

### File Formats
- **CSV**: UTF-8 encoding, comma-separated
- **JSON**: Valid JSON only (use JSON validator if unsure)

---

## 🐛 Troubleshooting

### "Module not found" Error
```bash
pip install --upgrade requests beautifulsoup4 pandas
```

### Network Issues
- Check internet connection
- Verify URL is correct
- Check firewall settings
- Some websites may block scraping

### File Not Found
- Use full file path or navigate using file dialog
- Check file permissions

### JSON Parse Error
- Validate JSON at: https://jsonlint.com/
- Use proper quotes (double quotes, not single)

---

## 📝 Code Structure

```
my_python_tool.py
├── ToolConfig          # Configuration and styling
├── OutputLogger        # Logging and output handling
├── WebScraperModule    # Web scraping functionality
├── DataAnalysisModule  # Data analysis tools
├── APIModule           # API interaction
├── FileModule          # File conversion and merging
└── MainApp             # Main UI application
```

---

## 🎓 Learning Resources

- **Requests Library**: https://requests.readthedocs.io/
- **BeautifulSoup**: https://www.crummy.com/software/BeautifulSoup/
- **Pandas**: https://pandas.pydata.org/docs/
- **Tkinter**: https://docs.python.org/3/library/tkinter.html

---

## 💻 System Requirements

- **OS**: Windows, macOS, Linux
- **Python**: 3.8 or higher
- **RAM**: 512MB minimum (1GB+ recommended)
- **Disk Space**: 100MB for dependencies

---

## 🚀 Advanced Usage

### Batch Processing
You can extend the tool to process multiple files:
```python
import glob

# Process all CSV files in a directory
for csv_file in glob.glob('data/*.csv'):
    df, stats = DataAnalysisModule.load_csv(csv_file)
    # Process each file
```

### Database Integration
Add SQLite support:
```python
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
```

### Scheduled Tasks
Use `schedule` library for automated operations:
```python
pip install schedule
```

---

## 📧 Support

For issues or questions:
1. Check the troubleshooting section
2. Review error messages in the output panel
3. Check library documentation
4. Verify file formats and API endpoints

---

## 📄 License

This tool is provided as-is for personal and educational use.

---

**Last Updated**: 2024-04-13
**Version**: 1.0
**Author**: Custom Build

