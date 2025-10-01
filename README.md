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
python3 -m venv .venv

# 2. Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

## ▶️ Usage

Run the main application:

```bash
source .venv/bin/activate
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

## 🛒 Bazarchic Products Database Tool

**Advanced Python tool for Bazarchic MySQL database operations with comprehensive product data extraction and CSV export capabilities.**

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#️-usage)
- [Directory Structure](#-directory-structure)
- [Database Schema](#-database-schema)
- [CSV Export Formats](#-csv-export-formats)
- [Examples](#-examples)
- [Troubleshooting](#-troubleshooting)
- [Technical Details](#-technical-details)

## 🚀 Features

### Core Database Operations

- **Database Analysis**: List all 870+ tables and analyze structure
- **Product Information**: Detailed product table analysis with field mapping
- **Comprehensive Exports**: Multiple CSV export formats with technical specifications

### Advanced Data Extraction

- **Technical Specifications**: Extract capacity, expiration dates, durability dates, and ingredients
- **Deep Database Relationships**: Uses proper JOIN queries across multiple tables
- **Multi-language Support**: Handles French, English, German, Dutch, Spanish, and Italian data

### Export Capabilities

- **Standard Exports**: All products or filtered subsets
- **Comprehensive Format**: 37-column CSV with complete technical specifications
- **EAN Search**: Find and export products by barcode
- **Batch Processing**: Memory-efficient processing for large datasets

### Data Sources

- **181,393 products** with capacity data
- **68,081 products** with DDM (Date de durabilité minimale)
- **19,409 products** with DLC (Date limite de consommation)
- **Unique ingredients** per product via database relationships

## 🚀 Quick Start

```bash
# 1. Clone and setup
git clone <repository-url>
cd pythondb_bazarchic

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or .venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure database (see Configuration section)
# Edit .env file with your database credentials

# 5. Run the application
python main.py
```

## 📦 Installation

### Prerequisites

- **Python 3.8+**
- **MySQL Database Access** (bazarshop_base)
- **Network Access** to pp-lb.bazarchic.com

### Virtual Environment Setup

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

The project uses these Python packages:

```
mysql-connector-python==9.4.0  # MySQL database connector
python-dotenv==1.1.1           # Environment variable management
pandas==2.3.2                  # Data manipulation and CSV export
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
DB_HOST=pp-lb.bazarchic.com
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=bazarshop_base
DB_PORT=3306
```

### Database Connection

The tool connects to the Bazarchic MySQL database via ProxySQL. Ensure you have:

- Valid database credentials
- Network access to the database server
- Appropriate firewall/VPN configuration if required

## ▶️ Usage

### Interactive Menu

Run the main application to access the interactive menu:

```bash
source .venv/bin/activate
python main.py
```

### Menu Options

```
📋 Available Operations:
1. List all tables in the database
2. Analyze products table (fields and structure)
3. Export all products to CSV (original format)
4. Export sample products to CSV (10,000 products, original format)
5. Search products by EAN and save to CSV
6. 🎯 Export with COMPREHENSIVE HEADERS (your exact format)
7. 🎯 Export 10,000 products with COMPREHENSIVE HEADERS
8. 🎯 Search EAN with COMPREHENSIVE HEADERS
0. Exit
```

### Key Operations

#### 1. Database Analysis

- **Option 1**: Lists all 870+ database tables
- **Option 2**: Detailed analysis of the products table structure

#### 2. Standard CSV Exports

- **Option 3**: Full database export (8M+ products - ⚠️ Large file!)
- **Option 4**: Sample export (10,000 products)
- **Option 5**: EAN-based search and export

#### 3. Comprehensive CSV Exports (Recommended)

- **Option 6**: Full comprehensive export with 37 technical specification columns
- **Option 7**: Sample comprehensive export (10,000 products)
- **Option 8**: EAN search with comprehensive format

## 📁 Directory Structure

```
pythondb_bazarchic/
├── .env                           # Database configuration (create this)
├── .gitignore                     # Git ignore rules
├── .venv/                         # Python virtual environment
├── README.md                      # This documentation
├── requirements.txt               # Python dependencies
├── main.py                        # Main application (🚀 START HERE)
├── __pycache__/                   # Python cache (auto-generated)
├── *.csv                          # Generated CSV exports
└── eans.txt                       # Sample EAN codes for testing
```

### Core Files

| File               | Purpose              | Usage                                          |
| ------------------ | -------------------- | ---------------------------------------------- |
| `main.py`          | **Main application** | Run with `python main.py`                      |
| `.env`             | Database credentials | Configure before first use                     |
| `requirements.txt` | Python dependencies  | Install with `pip install -r requirements.txt` |
| `README.md`        | Documentation        | This file                                      |

## 🗄️ Database Schema

### Key Tables Used

The application intelligently queries multiple related tables:

```sql
-- Main product tables
produits                        -- Base product information
produits_group                  -- Product group details
produits_marque                 -- Brand information
produits_familles              -- Product families
produits_gallery               -- Product images

-- Technical specifications (Advanced Feature)
produits_group_caracteristiques -- Product characteristics
caracteristiques               -- Characteristic definitions
dictionnaires_langues          -- Multi-language values

-- Category and classification
categories                     -- Product categories
```

### Database Statistics

- **Total Tables**: 870+
- **Total Products**: 8,324,637
- **Products with EAN**: 3,145,079 (37.8%)
- **Technical Specs Available**: 181,393+ products
- **Multi-language Support**: 6 languages

## 📊 CSV Export Formats

### Standard Format (Options 3-5)

Basic product export with 26 core fields including:

- Product ID, EAN, Reference, Prices
- Descriptions, Status, Weight
- Keywords, Timestamps, etc.

### Comprehensive Format (Options 6-8) ⭐ **Recommended**

Advanced 37-column format with complete technical specifications:

| Column                            | Technical Field                    | Data Source              |
| --------------------------------- | ---------------------------------- | ------------------------ |
| Capacité                          | `technical_spec_1_capacity`        | Database characteristics |
| DLC (Date limite de consommation) | `technical_spec_1_expiration_date` | Database characteristics |
| DDM (Date de durabilité minimale) | `technical_spec_1_durability_date` | Database characteristics |
| Ingrédients                       | `technical_spec_1_ingredients`     | Database characteristics |
| Images (10 columns)               | `media_1` to `media_10`            | CDN URLs                 |
| Brand, Category, Description      | Various                            | Proper table JOINs       |

## 💡 Examples

### Example 1: Quick Product Analysis

```bash
python main.py
# Choose option 2: Analyze products table
```

Output:

```
📊 Products Table Analysis:
==================================================
Total products: 8,324,637
Products with EAN: 3,145,079 (37.8%)
Total fields: 26
```

### Example 2: EAN Search with Comprehensive Data

```bash
python main.py
# Choose option 8: Search EAN with COMPREHENSIVE HEADERS
# Enter EAN: 7290015070379
```

Generated CSV includes:

- **Capacity**: "120 ml" (from database)
- **Ingredients**: Full detailed ingredient list
- **Images**: 10 high-resolution product images
- **Brand**: "Bio Spa"
- **Complete technical specifications**

### Example 3: Sample Export for Testing

```bash
python main.py
# Choose option 7: Export 10,000 products with COMPREHENSIVE HEADERS
```

Perfect for:

- Testing the format
- Data analysis samples
- Quick validation

### Example 4: Multiple EAN Search

```bash
python main.py
# Choose option 8, then option b (multiple EANs)
# Enter: 7290015070379,7640112441273,3760128680863
```

## 🔧 Troubleshooting

### Common Issues

#### Connection Problems

```bash
❌ Database connection failed: Access denied
```

**Solution**: Check your `.env` file credentials

#### Large File Issues

```bash
⚠️ Memory error during export
```

**Solution**: Use sample exports (options 4 or 7) or increase batch size

#### Missing Data

```bash
Empty columns in CSV export
```

**Solution**: Use comprehensive format (options 6-8) for complete data

### Debug Commands

Check your environment:

```bash
# Test database connection
python -c "from main import BazarchicDB; db = BazarchicDB(); print('✅ Connection OK' if db.connection else '❌ Connection Failed')"

# Verify environment variables
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(f'Host: {os.getenv("DB_HOST")}')"
```

### Performance Tips

1. **Use sample exports** for testing (options 4, 7)
2. **Batch processing** is automatic for large exports
3. **EAN searches** are fastest for specific products
4. **Comprehensive format** provides the most complete data

## 🔬 Technical Details

### Database Extraction Methods

The application uses advanced SQL JOINs to extract technical specifications:

```python
# Capacity extraction
get_capacity_from_product()    # Uses produits_group_caracteristiques
get_dlc_from_product()         # Extracts expiration dates
get_ddm_from_product()         # Extracts durability dates
get_ingredients_from_product() # Extracts ingredient lists
```

### Multi-language Support

Technical specifications are available in:

- 🇫🇷 French (Contenance, DDM, Ingrédients)
- 🇬🇧 English (Capacity, DDM, Ingredients)
- 🇩🇪 German (Kapazität, Mindesthaltbarkeitsdatum)
- 🇳🇱 Dutch (Capaciteit, Minimale houdbaarheidsdatum)
- 🇪🇸 Spanish (Capacidad, Fecha de durabilidad)
- 🇮🇹 Italian (Capacità, Data minima di durabilità)

### Performance Specifications

| Operation           | Typical Time  | File Size |
| ------------------- | ------------- | --------- |
| Sample Export (10K) | 30-60 seconds | 1-5 MB    |
| EAN Search          | 5-15 seconds  | 0.1-1 MB  |
| Full Export (8M+)   | 2-6 hours     | 1-3 GB    |
| Database Analysis   | 10-30 seconds | N/A       |

### Memory Management

- **Batch Processing**: 10,000-50,000 products per batch
- **Progress Tracking**: Real-time progress for large operations
- **Memory Efficient**: Streaming processing prevents memory overflow

## 📞 Support

For issues or questions:

1. **Check this README** for common solutions
2. **Test with sample exports** before large operations
3. **Use comprehensive format** (options 6-8) for complete data
4. **Check database connectivity** if experiencing connection issues

---

**Version**: 2.0 | **Last Updated**: October 2025 | **Database**: bazarshop_base

### 2. Environment Variables

The database connection uses the following environment variables from `.env`:

```env
DB_HOST=
DB_USER=
DB_PASSWORD=
DB_NAME=
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
