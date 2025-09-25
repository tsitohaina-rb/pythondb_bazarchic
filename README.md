# Bazarchic Products Database Tool

Simple tool to work with the Bazarchic MySQL database for product management.

## 🚀 Features

- List all tables in the database
- Analyze products table structure and fields
- Export all products to CSV
- Search products by EAN codes and save results to CSV

## � Setup

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

## ▶️ Usage

Run the main application:

```bash
source venv/bin/activate
python main.py
```

### Menu Options:

1. **List all tables** - Shows all 870+ tables in the database
2. **Analyze products table** - Shows structure, fields, and sample data
3. **Export all products** - Export all 8M+ products to CSV (⚠️ Large file!)
4. **Export sample products** - Export first 10,000 products to CSV
5. **Search by EAN** - Search products by EAN codes and save to CSV

## 📊 Database Info

- **Database**: bazarshop_base
- **Total Products**: 8,324,637
- **Products with EAN**: 3,145,079 (37.8%)
- **Product Fields**: 26 columns

## 📋 Example EAN Codes

Try these EAN codes for testing:

- `3664436019363`
- `3014151002667`
- `3014151002797`

## 📁 Files

- `main.py` - Main application (run this)
- `.env` - Database credentials
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Dependencies

- mysql-connector-python - Database connection
- python-dotenv - Environment variables
- pandas - CSV export functionality

## Setup

### 1. Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Variables

The database connection uses the following environment variables from `.env`:

```env
DB_HOST=pp-lb.bazarchic.com
DB_USER=bazar
DB_PASSWORD=Tz#54!g
DB_NAME=bazarshop_base
DB_PORT=3306
```

## 📁 Project Files

### Core Export Tools

- **`export_products_csv.py`** - Main CSV export tool with multiple options
- **`search_by_ean.py`** - EAN search and export tool
- **`bulk_export_products.py`** - JSON bulk export (alternative format)

### Connection & Testing Tools

- **`db_connection.py`** - Basic database connection and table listing
- **`test_connection.py`** - Detailed connection testing with diagnostics
- **`get_products.py`** - Sample product retrieval tool
- **`get_products_with_ean.py`** - EAN products analysis tool

### Configuration Files

- **`.env`** - Database connection credentials
- **`requirements.txt`** - Python dependencies

## 🛠️ Usage

### 1. Export All Products to CSV

```bash
source venv/bin/activate
python export_products_csv.py
```

**Options:**

1. Export ALL products (8.3M+ - ⚠️ Large file: 1-3 GB)
2. Export products with EAN codes only (3.1M+)
3. Export first 10,000 products (sample)
4. Export first 10,000 products with EAN codes (sample)
5. Search by specific EAN code(s)
6. Custom export with your parameters

### 2. Search Products by EAN

```bash
source venv/bin/activate
python search_by_ean.py
```

**Search Options:**

- **Single EAN**: Search for one specific EAN code
- **Multiple EANs**: Comma-separated EAN codes
- **File Input**: Load EAN codes from text file (one per line)
- **Interactive**: Multiple searches in one session

**Example EAN codes in database:**

- `3664436019363` - Bandeau froncé motif marguerites
- `3014151002667`, `3014151002797`, etc.

### 3. Quick Database Overview

```bash
source venv/bin/activate
python db_connection.py  # List all tables
python test_connection.py  # Detailed connection info
```

## 📋 Product Fields (CSV Columns)

All CSV exports include these 26 fields:

| Field                 | Type         | Description                  |
| --------------------- | ------------ | ---------------------------- |
| `idproduit`           | int          | Unique product ID            |
| `idproduit_group`     | int          | Product group ID             |
| `ean`                 | varchar(100) | **EAN/Barcode**              |
| `ref`                 | varchar(255) | Product reference            |
| `prix`                | decimal      | Selling price                |
| `prix_public`         | decimal      | Public/retail price          |
| `prix_ha`             | float        | Purchase price               |
| `eco_taxe`            | decimal      | Eco tax                      |
| `poids`               | decimal      | Weight (kg)                  |
| `description_fr`      | text         | French description           |
| `status`              | enum         | Product status (on/off/base) |
| `virtuel`             | enum         | Virtual product (oui/non)    |
| `keywords`            | varchar      | SEO keywords                 |
| `updated_produits`    | timestamp    | Last update                  |
| ...and 12 more fields |              | Various IDs, dates, etc.     |

## 📈 Performance & File Sizes

### Sample Export Results:

- **10,000 products (all)**: ~1.01 MB CSV
- **10,000 products (EAN only)**: ~1.28 MB CSV
- **100 products search result**: ~0.44 KB CSV

### Estimated Full Export Sizes:

- **ALL products** (8.3M): ~800 MB - 3 GB CSV
- **EAN products** (3.1M): ~400 MB - 1.2 GB CSV

### Batch Processing:

- Default batch size: 10,000 products
- Large exports: 50,000 products per batch
- Memory efficient with progress tracking

## 🔍 EAN Search Examples

### Search Single EAN:

```bash
python search_by_ean.py
# Choose option 1, enter: 3664436019363
```

### Search Multiple EANs:

```bash
python search_by_ean.py
# Choose option 2, enter: 3664436019363,3014151002667,3014151002797
```

### Search from File:

Create `ean_codes.txt`:

```
3664436019363
3014151002667
3014151002797
```

Then run and choose option 3.

## ⚠️ Important Notes

1. **Large Exports**: Full database exports can take hours and create multi-GB files
2. **Memory Usage**: Batch processing keeps memory usage reasonable
3. **EAN Coverage**: Only 37.8% of products have EAN codes
4. **File Encoding**: All CSV files use UTF-8 encoding
5. **Progress Tracking**: All large operations show real-time progress

## Dependencies

- `mysql-connector-python==9.4.0` - MySQL database connector
- `python-dotenv==1.1.1` - Environment variable loading
- `pandas==2.3.2` - Data manipulation and CSV export

## Database Information

- **Host**: pp-lb.bazarchic.com
- **Database**: bazarshop_base
- **MySQL Version**: 5.7.40
- **Connection**: Via ProxySQL

## 🎯 Common Use Cases

1. **Full Product Export**: Get all products for analysis/backup
2. **EAN-Only Export**: Focus on products with barcodes
3. **EAN Lookup**: Find specific products by barcode
4. **Bulk EAN Search**: Process multiple EAN codes at once
5. **Product Sampling**: Get representative samples for testing

## 📞 Troubleshooting

If you encounter connection issues:

```bash
python test_connection.py  # Detailed diagnostics
python debug_env.py       # Environment variable debugging
```

Common issues:

- **Connection refused**: Check VPN/network access
- **Authentication failed**: Verify credentials in `.env`
- **Large file issues**: Use batch exports or reduce limits

````

## Files Description

### Core Files

- `.env` - Database connection credentials
- `requirements.txt` - Python dependencies
- `db_connection.py` - Main database connection script
- `test_connection.py` - Detailed connection testing with error handling
- `debug_env.py` - Environment variable debugging utility

### Scripts Usage

#### Main Database Connection

```bash
source venv/bin/activate
python db_connection.py
````

This script:

- Connects to the MySQL database
- Lists all 870 tables in the database
- Provides basic connection information

#### Test Connection (Recommended for troubleshooting)

```bash
source venv/bin/activate
python test_connection.py
```

This script provides:

- Detailed connection parameters display
- Comprehensive error handling and diagnostics
- Specific guidance for connection issues
- Table listing with count

#### Debug Environment Variables

```bash
source venv/bin/activate
python debug_env.py
```

Useful for troubleshooting environment variable loading issues.

## Database Information

- **Host**: pp-lb.bazarchic.com
- **Database**: bazarshop_base
- **Tables**: 870 tables
- **MySQL Version**: 5.7.40

### Key Tables (Examples)

- `produits` - Products
- `commandes` - Orders
- `membres` - Members/Users
- `categories` - Categories
- `stock_*` - Stock management tables
- `codebarre` - Barcodes (relevant for EAN lookups)

## Dependencies

- `mysql-connector-python==9.4.0` - MySQL database connector
- `python-dotenv==1.1.1` - Environment variable loading

## Notes

- The database contains 870 tables related to e-commerce operations
- Connection uses ProxySQL (indicated by error messages)
- The `codebarre` table is likely relevant for EAN-based product lookups
- All scripts include proper error handling and connection management

## Next Steps for API Development

For creating an API to get products by EAN, you'll likely want to:

1. Examine the `codebarre` table structure:

```python
cursor.execute("DESCRIBE codebarre")
```

2. Look at the `produits` table structure:

```python
cursor.execute("DESCRIBE produits")
```

3. Understand the relationship between barcodes and products

4. Create API endpoints using Flask/FastAPI to query products by EAN code
