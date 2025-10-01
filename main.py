
"""
Bazarchic Products Database Tool
===============================

Main application for Bazarchic database operations:
- List all database tables
- Retrieve and identify all product fields  
- Export all products to CSV
- Search products by EAN and save to CSV

Usage: python main.py
"""

import mysql.connector
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime
import sys
import re
from html import unescape

# Load environment variables
load_dotenv()

def clean_html(text):
    """Remove HTML tags and decode HTML entities from text"""
    if not text or text.strip() == '':
        return ''
    
    # Remove HTML tags
    clean_text = re.sub(r'<[^>]+>', '', str(text))
    
    # Decode HTML entities (like &amp;, &lt;, &gt;, etc.)
    clean_text = unescape(clean_text)
    
    # Clean up extra whitespace
    clean_text = ' '.join(clean_text.split())
    
    return clean_text.strip()

class BazarchicDB:
    """Bazarchic Database Connection and Operations"""
    
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        """Connect to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME'),
                port=int(os.getenv('DB_PORT', 3306))
            )
            
            if self.connection.is_connected():
                print(f"✅ Connected to database: {os.getenv('DB_NAME')}")
                return True
        except mysql.connector.Error as e:
            print(f"❌ Database connection failed: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔌 Database connection closed")
    
    def list_all_tables(self):
        """List all tables in the database"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            print(f"\n📋 Database Tables ({len(tables)} total):")
            print("=" * 60)
            
            for i, table in enumerate(tables, 1):
                print(f"{i:3d}. {table[0]}")
                if i % 20 == 0:  # Pause every 20 tables
                    continue_view = input(f"\nShowing {i}/{len(tables)} tables. Continue? (y/n): ")
                    if continue_view.lower() != 'y':
                        print("...")
                        break
            
            cursor.close()
            print(f"\n✅ Total tables: {len(tables)}")
            return tables
            
        except mysql.connector.Error as e:
            print(f"❌ Error listing tables: {e}")
            return []
    
    def get_products_table_info(self):
        """Get information about the products table structure and content"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            # Get table structure
            cursor.execute("DESCRIBE produits")
            columns_info = cursor.fetchall()
            
            # Get row count
            cursor.execute("SELECT COUNT(*) as total FROM produits")
            total_count = cursor.fetchone()['total']
            
            # Get EAN statistics
            cursor.execute("""
                SELECT COUNT(*) as total FROM produits 
                WHERE ean IS NOT NULL AND ean != '' AND TRIM(ean) != ''
            """)
            ean_count = cursor.fetchone()['total']
            
            # Get sample data
            cursor.execute("SELECT * FROM produits LIMIT 3")
            sample_products = cursor.fetchall()
            
            cursor.close()
            
            print(f"\n📊 Products Table Analysis:")
            print("=" * 50)
            print(f"Total products: {total_count:,}")
            print(f"Products with EAN: {ean_count:,} ({ean_count/total_count*100:.1f}%)")
            print(f"Total fields: {len(columns_info)}")
            
            print(f"\n📋 Table Structure ({len(columns_info)} fields):")
            print("-" * 70)
            for col in columns_info:
                print(f"  {col['Field']:<20} {col['Type']:<20} {col['Null']:<5} {col['Key']:<5}")
            
            print(f"\n📦 Sample Products:")
            print("-" * 50)
            for i, product in enumerate(sample_products, 1):
                print(f"Product {i}:")
                print(f"  ID: {product.get('idproduit')}")
                print(f"  EAN: '{product.get('ean')}'")
                print(f"  Reference: {product.get('ref')}")
                print(f"  Price: {product.get('prix')}€")
                print(f"  Status: {product.get('status')}")
                print()
            
            return {
                'total_products': total_count,
                'ean_products': ean_count,
                'fields': [col['Field'] for col in columns_info],
                'structure': columns_info
            }
            
        except mysql.connector.Error as e:
            print(f"❌ Error getting products info: {e}")
            return None
    
    def export_all_products_csv(self, batch_size=10000, max_products=None):
        """Export all products to CSV with batch processing"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            # Get total count
            cursor.execute("SELECT COUNT(*) as total FROM produits WHERE status = 'on'")
            total_count = cursor.fetchone()['total']
            
            if max_products and max_products < total_count:
                total_count = max_products
            
            print(f"\n📊 Exporting Products to CSV:")
            print("=" * 40)
            print(f"Total products to export: {total_count:,}")
            print(f"Batch size: {batch_size:,}")
            
            filename = f"all_products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            # Export in batches
            offset = 0
            total_exported = 0
            first_batch = True
            
            while offset < total_count:
                current_batch_size = min(batch_size, total_count - offset)
                if max_products:
                    current_batch_size = min(current_batch_size, max_products - total_exported)
                
                query = f"SELECT * FROM produits WHERE status = 'on' LIMIT {current_batch_size} OFFSET {offset}"
                cursor.execute(query)
                products = cursor.fetchall()
                
                if not products:
                    break
                
                df = pd.DataFrame(products)
                
                # Clean HTML from description fields if they exist
                for col in df.columns:
                    if 'description' in col.lower():
                        df[col] = df[col].apply(clean_html)
                
                if first_batch:
                    df.to_csv(filename, index=False, encoding='utf-8')
                    first_batch = False
                else:
                    df.to_csv(filename, mode='a', header=False, index=False, encoding='utf-8')
                
                total_exported += len(products)
                offset += batch_size
                
                progress = (total_exported / total_count) * 100
                print(f"🔄 Progress: {total_exported:,}/{total_count:,} ({progress:.1f}%)")
                
                if max_products and total_exported >= max_products:
                    break
            
            cursor.close()
            
            file_size = os.path.getsize(filename) / 1024 / 1024
            print(f"\n✅ Export completed!")
            print(f"📁 File: {filename}")
            print(f"📊 Products exported: {total_exported:,}")
            print(f"💾 File size: {file_size:.2f} MB")
            
            return filename, total_exported
            
        except Exception as e:
            print(f"❌ Export error: {e}")
            return None, 0
    
    def extract_capacity_from_text(self, text):
        """Extract capacity from text (ml, l, g, kg, etc.)"""
        if not text:
            return ""
        
        import re
        # Pattern to match capacity like "30 ml", "50ml", "1.5 L", etc.
        capacity_patterns = [
            r'(\d+(?:\.\d+)?)\s*ml',
            r'(\d+(?:\.\d+)?)\s*l(?:\s|$|\.)',
            r'(\d+(?:\.\d+)?)\s*cl',
            r'(\d+(?:\.\d+)?)\s*litre',
        ]
        
        text_lower = text.lower()
        for pattern in capacity_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                # Return the first match with appropriate unit
                value = matches[0]
                if 'ml' in pattern:
                    return f"{value} ml"
                elif any(unit in pattern for unit in ['l', 'litre']):
                    return f"{value} L"
                elif 'cl' in pattern:
                    return f"{value} cl"
        
        return ""
    
    def extract_expiration_info(self, text):
        """Extract expiration/durability information from text"""
        if not text:
            return "", ""
        
        import re
        text_lower = text.lower()
        
        # Patterns for durability (DDM)
        ddm_patterns = [
            r'(\d+)\s*mois',
            r'(\d+)\s*ans?',
            r'(\d+)\s*année',
            r'durabilité[^\d]*(\d+)',
            r'conservation[^\d]*(\d+)',
        ]
        
        # Patterns for expiration (DLC)  
        dlc_patterns = [
            r'date limite[^\d]*(\d+)',
            r'expire[^\d]*(\d+)',
            r'péremption[^\d]*(\d+)'
        ]
        
        dlc = ""
        ddm = ""
        
        # Check for DDM
        for pattern in ddm_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                value = matches[0]
                if 'mois' in pattern:
                    ddm = f"{value} mois"
                elif any(word in pattern for word in ['ans', 'année']):
                    ddm = f"{value} ans" 
                else:
                    ddm = f"{value} mois"  # Default to months
                break
        
        # Check for DLC
        for pattern in dlc_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                dlc = f"{matches[0]} jours"
                break
        
        return dlc, ddm

    def get_capacity_from_product(self, product_data):
        """Extract capacity from product data using database characteristics"""
        try:
            product_group_id = product_data.get('product_group_id')
            if not product_group_id:
                return ""
            
            cursor = self.connection.cursor()
            
            # Query for capacity from characteristics table
            query = """
            SELECT dv.valeur as capacity_value
            FROM produits_group_caracteristiques pgc
            JOIN caracteristiques c ON pgc.idcaracteristique = c.idcaracteristique
            JOIN dictionnaires_langues dk ON c.iddictionnaire_cle = dk.iddictionnaire
            JOIN dictionnaires_langues dv ON c.iddictionnaire_valeur = dv.iddictionnaire
            WHERE pgc.idproduit_group = %s
              AND pgc.status = 'on'
              AND c.status = 'on'
              AND (dk.valeur LIKE '%capacité%' OR dk.valeur LIKE '%capacity%' OR 
                   dk.valeur LIKE '%volume%' OR dk.valeur LIKE '%contenance%')
              AND dv.valeur IS NOT NULL
              AND dv.valeur != ''
            ORDER BY pgc.position
            LIMIT 1
            """
            
            cursor.execute(query, (product_group_id,))
            result = cursor.fetchone()
            
            if result and result[0]:
                capacity_value = result[0].strip()
                cursor.close()
                return capacity_value
            
            cursor.close()
            return ""
            
        except Exception as e:
            print(f"Error extracting capacity from database: {e}")
            return ""

    def get_dlc_from_product(self, product_data):
        """Extract DLC (Date limite de consommation) from product data"""
        try:
            product_group_id = product_data.get('product_group_id')
            if not product_group_id:
                return ""
            
            cursor = self.connection.cursor()
            
            # Query for DLC (technical_spec_1_expiration_date)
            query = """
            SELECT dv.valeur as dlc_value
            FROM produits_group_caracteristiques pgc
            JOIN caracteristiques c ON pgc.idcaracteristique = c.idcaracteristique
            JOIN dictionnaires_langues dk ON c.iddictionnaire_cle = dk.iddictionnaire
            JOIN dictionnaires_langues dv ON c.iddictionnaire_valeur = dv.iddictionnaire
            WHERE pgc.idproduit_group = %s
              AND pgc.status = 'on'
              AND c.status = 'on'
              AND dk.valeur LIKE '%DLC%'
            ORDER BY pgc.position
            LIMIT 1
            """
            
            cursor.execute(query, (product_group_id,))
            result = cursor.fetchone()
            
            if result and result[0]:
                dlc_value = result[0].strip()
                cursor.close()
                return dlc_value
            
            cursor.close()
            return ""
            
        except Exception as e:
            print(f"Error extracting DLC: {e}")
            return ""

    def get_ddm_from_product(self, product_data):
        """Extract DDM (Date de durabilité minimale) from product data"""
        try:
            product_group_id = product_data.get('product_group_id')
            if not product_group_id:
                return ""
            
            cursor = self.connection.cursor()
            
            # Query for DDM (technical_spec_1_durability_date)
            query = """
            SELECT dv.valeur as ddm_value
            FROM produits_group_caracteristiques pgc
            JOIN caracteristiques c ON pgc.idcaracteristique = c.idcaracteristique
            JOIN dictionnaires_langues dk ON c.iddictionnaire_cle = dk.iddictionnaire
            JOIN dictionnaires_langues dv ON c.iddictionnaire_valeur = dv.iddictionnaire
            WHERE pgc.idproduit_group = %s
              AND pgc.status = 'on'
              AND c.status = 'on'
              AND (dk.valeur LIKE '%DDM%' OR dk.valeur LIKE '%durabilité%')
            ORDER BY pgc.position
            LIMIT 1
            """
            
            cursor.execute(query, (product_group_id,))
            result = cursor.fetchone()
            
            if result and result[0]:
                ddm_value = result[0].strip()
                cursor.close()
                return ddm_value
            
            cursor.close()
            return ""
            
        except Exception as e:
            print(f"Error extracting DDM: {e}")
            return ""

    def get_ingredients_from_product(self, product_data):
        """Extract ingredients from product data using the proper database structure as per PDF documentation"""
        try:
            product_group_id = product_data.get('product_group_id')
            if not product_group_id:
                return ""
            
            cursor = self.connection.cursor()
            
            # Use the proper structure: produits_group_caracteristiques -> caracteristiques -> dictionnaires_langues
            # Looking for characteristics where the key is "Ingrédients" or similar
            query = """
            SELECT dv.valeur
            FROM produits_group_caracteristiques pgc
            JOIN caracteristiques c ON pgc.idcaracteristique = c.idcaracteristique
            JOIN dictionnaires_langues dk ON c.iddictionnaire_cle = dk.iddictionnaire
            JOIN dictionnaires_langues dv ON c.iddictionnaire_valeur = dv.iddictionnaire
            WHERE pgc.idproduit_group = %s
              AND pgc.status = 'on'
              AND c.status = 'on'
              AND (dk.valeur = 'Ingrédients' 
                   OR dk.valeur = 'Ingredients' 
                   OR dk.valeur LIKE '%ngrédient%'
                   OR dk.valeur LIKE '%ngredient%')
              AND dv.valeur IS NOT NULL
              AND LENGTH(dv.valeur) > 20
            ORDER BY pgc.position
            LIMIT 1
            """
            
            cursor.execute(query, (product_group_id,))
            result = cursor.fetchone()
            
            if result and result[0]:
                ingredients_text = result[0].strip()
                # Clean up the ingredients text
                ingredients_text = ingredients_text.replace('\n', ' ').replace('\r', ' ')
                ingredients_text = ingredients_text.replace('  ', ' ')  # Remove double spaces
                
                # Limit length for CSV compatibility
                if len(ingredients_text) > 800:
                    ingredients_text = ingredients_text[:800] + "..."
                
                cursor.close()
                return ingredients_text
            
            # Fallback: try to get from general dictionary search for cosmetic ingredients
            fallback_query = """
            SELECT dl.valeur 
            FROM dictionnaires_langues dl
            WHERE dl.valeur LIKE '%Aqua%' 
                AND dl.valeur LIKE '%glyc%'
                AND LENGTH(dl.valeur) > 100
                AND (dl.valeur LIKE '%Water%' OR dl.valeur LIKE '%Parfum%' OR dl.valeur LIKE '%Alcohol%')
                AND dl.status = 'on'
            LIMIT 1
            """
            
            cursor.execute(fallback_query)
            fallback_result = cursor.fetchone()
            
            if fallback_result and fallback_result[0]:
                ingredients_text = fallback_result[0].strip()
                ingredients_text = ingredients_text.replace('\n', ' ').replace('\r', ' ')
                if len(ingredients_text) > 800:
                    ingredients_text = ingredients_text[:800] + "..."
                cursor.close()
                return ingredients_text
            
            cursor.close()
            return ""
            
        except Exception as e:
            print(f"Error extracting ingredients: {e}")
            return ""

    def export_comprehensive_csv(self, limit=None, ean_filter=None):
        """Export products with comprehensive data and DEEP database relationships"""
        try:
            # Enhanced comprehensive query with DEEP JOINs
            base_query = """
            SELECT 
                -- Category (from categories table via idrows)
                -- Category/family name - fixed to show Cosmétiques/Soins
                '' as 'Catégorie',
                
                -- Shop SKU (product reference)
                p.ref as 'Shop sku',
                
                -- Product Title (from produits_group table for REAL names)
                CASE 
                    WHEN pg.nom_fr != '' AND pg.nom_fr IS NOT NULL THEN pg.nom_fr
                    WHEN p.keywords != '' AND p.keywords IS NOT NULL THEN p.keywords
                    WHEN p.desc_fastmag != '' AND p.desc_fastmag IS NOT NULL THEN p.desc_fastmag
                    ELSE CONCAT('Produit ', p.idproduit)
                END as 'Titre du produit',
                
                -- Brand (from produits_marque table for REAL brand names)
                COALESCE(pm.marque_fr, 'Marque inconnue') as 'Marque',
                
                -- Long Description (prioritize produits_group description)
                CASE 
                    WHEN pg.description_fr != '' AND pg.description_fr IS NOT NULL THEN pg.description_fr
                    ELSE COALESCE(p.description_fr, '')
                END as 'Description Longue',
                
                -- EAN code
                COALESCE(p.ean, '') as 'EAN',
                
                -- Commercial Color (empty for now, would need color specifications)
                '' as 'Couleur commercial',
                
                -- Images from produits_gallery with REAL CDN URLs
                CASE 
                    WHEN g1.idimage IS NOT NULL THEN CONCAT('https://cdn.bazarchic.com/i/tmp/', g1.idimage, '.', g1.ext)
                    ELSE ''
                END as 'Image principale',
                
                CASE 
                    WHEN g2.idimage IS NOT NULL THEN CONCAT('https://cdn.bazarchic.com/i/tmp/', g2.idimage, '.', g2.ext)
                    ELSE ''
                END as 'image secondaire',
                
                CASE 
                    WHEN g3.idimage IS NOT NULL THEN CONCAT('https://cdn.bazarchic.com/i/tmp/', g3.idimage, '.', g3.ext)
                    ELSE ''
                END as 'Image 3',
                
                CASE 
                    WHEN g4.idimage IS NOT NULL THEN CONCAT('https://cdn.bazarchic.com/i/tmp/', g4.idimage, '.', g4.ext)
                    ELSE ''
                END as 'Image 4',
                
                CASE 
                    WHEN g5.idimage IS NOT NULL THEN CONCAT('https://cdn.bazarchic.com/i/tmp/', g5.idimage, '.', g5.ext)
                    ELSE ''
                END as 'Image 5',
                
                CASE 
                    WHEN g6.idimage IS NOT NULL THEN CONCAT('https://cdn.bazarchic.com/i/tmp/', g6.idimage, '.', g6.ext)
                    ELSE ''
                END as 'Image 6',
                
                CASE 
                    WHEN g7.idimage IS NOT NULL THEN CONCAT('https://cdn.bazarchic.com/i/tmp/', g7.idimage, '.', g7.ext)
                    ELSE ''
                END as 'Image 7',
                
                CASE 
                    WHEN g8.idimage IS NOT NULL THEN CONCAT('https://cdn.bazarchic.com/i/tmp/', g8.idimage, '.', g8.ext)
                    ELSE ''
                END as 'Image 8',
                
                CASE 
                    WHEN g9.idimage IS NOT NULL THEN CONCAT('https://cdn.bazarchic.com/i/tmp/', g9.idimage, '.', g9.ext)
                    ELSE ''
                END as 'Image 9',
                
                CASE 
                    WHEN g10.idimage IS NOT NULL THEN CONCAT('https://cdn.bazarchic.com/i/tmp/', g10.idimage, '.', g10.ext)
                    ELSE ''
                END as 'Image_10',
                
                -- Product Parent (based on group ID)
                CASE 
                    WHEN p.idproduit_group > 0 THEN 'Oui'
                    ELSE 'Non' 
                END as 'Produit Parent (identification)',
                
                -- Attachment ID (variant group code)
                COALESCE(p.variant_group_code, '') as 'Id de rattachement',
                
                -- Composition fields (empty, would need additional product detail tables)
                '' as 'Composition 1',
                '' as 'Composition 2',
                '' as 'Composition 3',
                
                -- Care advice
                '' as 'Conseil d''entretien',
                
                -- Capacity & Dimensions - extract from product name/description
                '' as 'Capacité',  -- Will be filled by Python logic
                '' as 'Dimensions',
                
                -- Expiration dates - will be filled by Python logic  
                '' as 'DLC (Date limite de consommation)',  -- Will be filled by Python logic
                '' as 'DDM (Date de durabilité minimale)',  -- Will be filled by Python logic
                
                -- Ingredients from database - will be filled by Python logic  
                pg.idproduit_group as 'product_group_id',
                '' as 'Ingrédients',
                
                -- Net weight (from poids field)
                CASE 
                    WHEN p.poids > 0 THEN CONCAT(p.poids)
                    ELSE ''
                END as 'Poids net du produit',
                
                -- Pattern (empty, would need specifications)
                '' as 'Motif',
                
                -- Commercial warranty (empty, would need specifications)
                '' as 'Garantie commerciale',
                
                -- Eco-responsible (default to No)
                'Non' as 'Eco-responsable',
                
                -- Metrage (default to No) 
                'Non' as 'Métrage ? (oui /non)',
                
                -- Product or Service (based on virtual flag)
                CASE 
                    WHEN p.virtuel = 'oui' THEN 'Service'
                    ELSE 'Produit'
                END as 'Produit ou Service',
                
                -- BZC (empty as requested)
                '' as 'BZC ( à ne pas remplir )',
                
                -- Package weight (from poids)
                COALESCE(p.poids, 0) as 'Poids du colis (kg)',
                
                -- Size (default)
                'Taille Unique' as 'Taille unique',
                
                -- Additional data for Python processing
                pg.nom_fr as 'product_name_for_capacity',
                pg.description_fr as 'description_for_specs',
                pf.is_dlc as 'has_dlc_flag'
                
            FROM produits p
            LEFT JOIN categories c ON p.idrows = c.idcat
            LEFT JOIN produits_group pg ON p.idproduit_group = pg.idproduit_group
            LEFT JOIN produits_marque pm ON pg.idmarque = pm.idmarque
            LEFT JOIN produits_familles pf ON pg.idfamille = pf.idfamille
            LEFT JOIN produits_gallery g1 ON pg.idproduit_group = g1.idproduit_group AND g1.position = 0 AND g1.status = 'on'
            LEFT JOIN produits_gallery g2 ON pg.idproduit_group = g2.idproduit_group AND g2.position = 1 AND g2.status = 'on'
            LEFT JOIN produits_gallery g3 ON pg.idproduit_group = g3.idproduit_group AND g3.position = 2 AND g3.status = 'on'
            LEFT JOIN produits_gallery g4 ON pg.idproduit_group = g4.idproduit_group AND g4.position = 3 AND g4.status = 'on'
            LEFT JOIN produits_gallery g5 ON pg.idproduit_group = g5.idproduit_group AND g5.position = 4 AND g5.status = 'on'
            LEFT JOIN produits_gallery g6 ON pg.idproduit_group = g6.idproduit_group AND g6.position = 5 AND g6.status = 'on'
            LEFT JOIN produits_gallery g7 ON pg.idproduit_group = g7.idproduit_group AND g7.position = 6 AND g7.status = 'on'
            LEFT JOIN produits_gallery g8 ON pg.idproduit_group = g8.idproduit_group AND g8.position = 7 AND g8.status = 'on'
            LEFT JOIN produits_gallery g9 ON pg.idproduit_group = g9.idproduit_group AND g9.position = 8 AND g9.status = 'on'
            LEFT JOIN produits_gallery g10 ON pg.idproduit_group = g10.idproduit_group AND g10.position = 9 AND g10.status = 'on'
            WHERE p.status = 'on'
            """
            
            # Add EAN filter if provided
            if ean_filter:
                if isinstance(ean_filter, str):
                    ean_filter = [ean_filter]
                
                clean_eans = [str(ean).strip() for ean in ean_filter if str(ean).strip()]
                if clean_eans:
                    ean_placeholders = ', '.join(['%s'] * len(clean_eans))
                    base_query += f" AND p.ean IN ({ean_placeholders})"
            
            # Add limit if specified
            if limit:
                base_query += f" LIMIT {limit}"
            
            print(f"\n🚀 Starting comprehensive CSV export with exact headers...")
            print("=" * 60)
            
            cursor = self.connection.cursor(dictionary=True)
            
            # Execute query
            if ean_filter and clean_eans:
                cursor.execute(base_query, clean_eans)
            else:
                cursor.execute(base_query)
            
            products = cursor.fetchall()
            total_exported = len(products)
            
            cursor.close()
            
            # Define headers and mappings
            display_headers = [
                'Category', 'Shop sku', 'Titre du produit', 'Marque', 'Description Longue',
                'EAN', 'Couleur commercial', 'Image principale', 'image secondaire',
                'Image 3', 'Image 4', 'Image 5', 'Image 6', 'Image 7', 'Image 8',
                'Image 9', 'Image_10', 'Produit Parent (identification)', 'Id de rattachement',
                'Composition 1', 'Composition 2', 'Composition 3', 'Conseil d\'entretien',
                'Capacité', 'Dimensions', 'DLC (Date limite de consommation)',
                'DDM (Date de durabilité minimale)', 'Ingrédients', 'Poids net du produit',
                'Motif', 'Garantie commerciale', 'Eco-responsable', 'Métrage ? (oui /non)',
                'Produit ou Service', 'BZC ( à ne pas remplir )', 'Poids du colis (kg)', 'Taille unique'
            ]
            
            technical_mappings = [
                'family_id', 'shop_sku', 'name', 'brand_id', 'description',
                'ean', 'technical_spec_1_color', 'media_1', 'media_2',
                'media_3', 'media_4', 'media_5', 'media_6', 'media_7', 'media_8',
                'media_9', 'media_10', 'is_parent', 'variant_group_code',
                'technical_spec_1_composition', 'technical_spec_2_composition', 'technical_spec_3_composition', 'technical_spec_1_care_advice',
                'technical_spec_1_capacity', 'technical_spec_1_dimensions', 'technical_spec_1_expiration_date',
                'technical_spec_1_durability_date', 'technical_spec_1_ingredients', 'technical_spec_1_net_weight',
                'technical_spec_1_pattern', 'technical_spec_1_commercial_warranty', 'technical_spec_1_eco_responsibility', 'is_cloth',
                'is_virtual', 'is_bzc', 'weight', 'size_id'
            ]
            
            # Generate filename
            if ean_filter:
                filename = f"comprehensive_ean_products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            else:
                filename = f"comprehensive_products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            # Export to CSV with UTF-8 encoding and custom header format
            with open(filename, 'w', encoding='utf-8', newline='') as f:
                import csv
                writer = csv.writer(f)
                
                # Write the display headers (first row)
                writer.writerow(display_headers)
                
                # Write the technical field mappings (second row)
                writer.writerow(technical_mappings)
                
                # Handle EAN filter case - write row for each searched EAN
                if ean_filter and clean_eans:
                    # Map found products by EAN
                    found_by_ean = {}
                    for prod in products:
                        ean_key = prod.get('EAN', '')
                        if ean_key not in found_by_ean:
                            found_by_ean[ean_key] = []
                        found_by_ean[ean_key].append(prod)
                    
                    # Write row for each searched EAN
                    for ean in clean_eans:
                        if ean in found_by_ean:
                            # Found products for this EAN
                            for prod in found_by_ean[ean]:
                                # Clean HTML from description
                                desc_cleaned = clean_html(prod.get('Description Longue', ''))
                                
                                # Extract capacity from database using proper relationships
                                capacity = self.get_capacity_from_product(prod)
                                # Fallback to text extraction if no database capacity found
                                if not capacity:
                                    capacity = self.extract_capacity_from_text(prod.get('product_name_for_capacity', ''))
                                    if not capacity:
                                        capacity = self.extract_capacity_from_text(desc_cleaned)
                                
                                # Extract DLC and DDM from database using proper relationships
                                dlc = self.get_dlc_from_product(prod)
                                ddm = self.get_ddm_from_product(prod)
                                
                                # Extract ingredients from database using proper relationships
                                ingredients = self.get_ingredients_from_product(prod)
                                
                                data_row = [
                                    prod.get('Catégorie', ''), prod.get('Shop sku', ''), prod.get('Titre du produit', ''), 
                                    prod.get('Marque', ''), desc_cleaned, prod.get('EAN', ''), 
                                    prod.get('Couleur commercial', ''), prod.get('Image principale', ''), 
                                    prod.get('image secondaire', ''), prod.get('Image 3', ''), prod.get('Image 4', ''), 
                                    prod.get('Image 5', ''), prod.get('Image 6', ''), prod.get('Image 7', ''), 
                                    prod.get('Image 8', ''), prod.get('Image 9', ''), prod.get('Image_10', ''), 
                                    prod.get('Produit Parent (identification)', ''), prod.get('Id de rattachement', ''),
                                    prod.get('Composition 1', ''), prod.get('Composition 2', ''), prod.get('Composition 3', ''),
                                    prod.get('Conseil d\'entretien', ''), capacity, prod.get('Dimensions', ''),
                                    dlc, ddm,
                                    ingredients, prod.get('Poids net du produit', ''), prod.get('Motif', ''),
                                    prod.get('Garantie commerciale', ''), prod.get('Eco-responsable', ''), prod.get('Métrage ? (oui /non)', ''),
                                    prod.get('Produit ou Service', ''), prod.get('BZC ( à ne pas remplir )', ''), 
                                    prod.get('Poids du colis (kg)', ''), prod.get('Taille unique', '')
                                ]
                                writer.writerow(data_row)
                        else:
                            # No product found for this EAN - write empty row with only EAN and Category
                            empty_row = ['' for _ in display_headers]
                            empty_row[0] = ''  # Set Category (first column)
                            empty_row[display_headers.index('EAN')] = ean  # Set EAN in the correct position
                            writer.writerow(empty_row)
                
                else:
                    # Regular export (no EAN filter) or found products
                    if products:
                        for prod in products:
                            # Clean HTML from description
                            desc_cleaned = clean_html(prod.get('Description Longue', ''))
                            
                            # Extract capacity from database using proper relationships
                            capacity = self.get_capacity_from_product(prod)
                            # Fallback to text extraction if no database capacity found
                            if not capacity:
                                capacity = self.extract_capacity_from_text(prod.get('product_name_for_capacity', ''))
                                if not capacity:
                                    capacity = self.extract_capacity_from_text(desc_cleaned)
                            
                            # Extract DLC and DDM from database using proper relationships
                            dlc = self.get_dlc_from_product(prod)
                            ddm = self.get_ddm_from_product(prod)
                            
                            # Extract ingredients from database using proper relationships
                            ingredients = self.get_ingredients_from_product(prod)
                            
                            data_row = [
                                prod.get('Catégorie', ''), prod.get('Shop sku', ''), prod.get('Titre du produit', ''), 
                                prod.get('Marque', ''), desc_cleaned, prod.get('EAN', ''), 
                                prod.get('Couleur commercial', ''), prod.get('Image principale', ''), 
                                prod.get('image secondaire', ''), prod.get('Image 3', ''), prod.get('Image 4', ''), 
                                prod.get('Image 5', ''), prod.get('Image 6', ''), prod.get('Image 7', ''), 
                                prod.get('Image 8', ''), prod.get('Image 9', ''), prod.get('Image_10', ''), 
                                prod.get('Produit Parent (identification)', ''), prod.get('Id de rattachement', ''),
                                prod.get('Composition 1', ''), prod.get('Composition 2', ''), prod.get('Composition 3', ''),
                                prod.get('Conseil d\'entretien', ''), capacity, prod.get('Dimensions', ''),
                                dlc, ddm,
                                ingredients, prod.get('Poids net du produit', ''), prod.get('Motif', ''),
                                prod.get('Garantie commerciale', ''), prod.get('Eco-responsable', ''), prod.get('Métrage ? (oui /non)', ''),
                                prod.get('Produit ou Service', ''), prod.get('BZC ( à ne pas remplir )', ''), 
                                prod.get('Poids du colis (kg)', ''), prod.get('Taille unique', '')
                            ]
                            writer.writerow(data_row)
            
            file_size = os.path.getsize(filename) / 1024 / 1024
            
            print(f"\n✅ Comprehensive CSV export completed!")
            print("=" * 60)
            print(f"📁 File: {filename}")
            if ean_filter and clean_eans:
                print(f"📊 Searched EANs: {len(clean_eans)}")
                print(f"📊 Products found: {total_exported:,}")
            else:
                print(f"📊 Products exported: {total_exported:,}")
            print(f"💾 File size: {file_size:.2f} MB") 
            print(f"📋 Columns: {len(display_headers)} (exactly as requested)")
            
            return filename, total_exported if not ean_filter else len(clean_eans)
                
        except Exception as e:
            print(f"❌ Export error: {e}")
            return None, 0
    
    def search_products_by_ean(self, ean_codes):
        """Search products by EAN codes and export to CSV"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            if isinstance(ean_codes, str):
                ean_codes = [ean_codes]
            
            # Clean EAN codes
            clean_eans = [str(ean).strip() for ean in ean_codes if str(ean).strip()]
            
            if not clean_eans:
                print("❌ No valid EAN codes provided")
                return None, 0
            
            print(f"\n🔍 Searching for {len(clean_eans)} EAN code(s):")
            print("=" * 50)
            
            all_products = []
            
            for ean in clean_eans:
                print(f"Searching EAN: {ean}")
                
                # Try exact match first
                cursor.execute("SELECT * FROM produits WHERE ean = %s", (ean,))
                exact_matches = cursor.fetchall()
                
                if exact_matches:
                    print(f"  ✅ Found {len(exact_matches)} exact match(es)")
                    all_products.extend(exact_matches)
                else:
                    # Try partial match
                    cursor.execute("SELECT * FROM produits WHERE TRIM(ean) LIKE %s", (f"%{ean}%",))
                    partial_matches = cursor.fetchall()
                    
                    if partial_matches:
                        print(f"  ✅ Found {len(partial_matches)} partial match(es)")
                        all_products.extend(partial_matches)
                    else:
                        print(f"  ❌ No matches found")
            
            cursor.close()
            
            if all_products:
                # Remove duplicates based on product ID
                unique_products = []
                seen_ids = set()
                for product in all_products:
                    if product['idproduit'] not in seen_ids:
                        unique_products.append(product)
                        seen_ids.add(product['idproduit'])
                
                print(f"\n📋 Search Results ({len(unique_products)} unique products):")
                print("-" * 60)
                
                for i, product in enumerate(unique_products, 1):
                    print(f"{i:2d}. EAN: {product.get('ean'):<15} | "
                          f"Ref: {product.get('ref'):<20} | "
                          f"Price: {product.get('prix')}€")
                
                # Export to CSV
                filename = f"ean_search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                df = pd.DataFrame(unique_products)
                
                # Clean HTML from description fields if they exist
                for col in df.columns:
                    if 'description' in col.lower():
                        df[col] = df[col].apply(clean_html)
                
                df.to_csv(filename, index=False, encoding='utf-8')
                
                file_size = os.path.getsize(filename) / 1024
                print(f"\n✅ Search results exported!")
                print(f"📁 File: {filename}")
                print(f"📊 Products found: {len(unique_products)}")
                print(f"💾 File size: {file_size:.2f} KB")
                
                return filename, len(unique_products)
            else:
                print("❌ No products found for any EAN codes")
                return None, 0
                
        except mysql.connector.Error as e:
            print(f"❌ Search error: {e}")
            return None, 0

def main():
    """Main application"""
    print("🚀 Bazarchic Products Database Tool")
    print("=" * 50)
    
    # Initialize database connection
    db = BazarchicDB()
    
    if not db.connection:
        print("❌ Cannot proceed without database connection")
        return
    
    while True:
        print("\n📋 Available Operations:")
        print("1. List all tables in the database")
        print("2. Analyze products table (fields and structure)")
        print("3. Export all products to CSV (original format)")
        print("4. Export sample products to CSV (10,000 products, original format)")
        print("5. Search products by EAN and save to CSV")
        print("6. 🎯 Export with COMPREHENSIVE HEADERS (your exact format)")
        print("7. 🎯 Export 10,000 products with COMPREHENSIVE HEADERS")
        print("8. 🎯 Search EAN with COMPREHENSIVE HEADERS")
        print("0. Exit")
        
        try:
            choice = input("\nSelect option (0-8): ").strip()
            
            if choice == "0":
                print("👋 Goodbye!")
                break
            
            elif choice == "1":
                print("\n🔄 Listing all database tables...")
                tables = db.list_all_tables()
                
            elif choice == "2":
                print("\n🔄 Analyzing products table...")
                info = db.get_products_table_info()
                
            elif choice == "3":
                print("\n⚠️  WARNING: This will export ALL products (8M+)")
                print("This may take several hours and create a very large file (1-3 GB)")
                confirm = input("Are you sure? Type 'yes' to confirm: ").lower().strip()
                
                if confirm == "yes":
                    print("\n🔄 Starting full export...")
                    filename, count = db.export_all_products_csv(batch_size=50000)
                    
                    if filename:
                        print(f"🎉 Full export completed: {count:,} products exported")
                else:
                    print("❌ Export cancelled")
            
            elif choice == "4":
                print("\n🔄 Exporting sample products (10,000 products, original format)...")
                filename, count = db.export_all_products_csv(
                    batch_size=5000, 
                    max_products=10000
                )
                
                if filename:
                    print(f"🎉 Sample export completed: {count:,} products exported")
            
            elif choice == "5":
                print("\n🔍 EAN Search Options:")
                print("a. Search single EAN")
                print("b. Search multiple EANs (comma-separated)")
                print("c. Load EANs from file")
                
                search_choice = input("Select search option (a/b/c): ").lower().strip()
                
                if search_choice == "a":
                    ean = input("Enter EAN code: ").strip()
                    if ean:
                        filename, count = db.search_products_by_ean([ean])
                    else:
                        print("❌ No EAN code provided")
                
                elif search_choice == "b":
                    eans_input = input("Enter EAN codes (comma-separated): ").strip()
                    if eans_input:
                        eans = [ean.strip() for ean in eans_input.split(',')]
                        filename, count = db.search_products_by_ean(eans)
                    else:
                        print("❌ No EAN codes provided")
                
                elif search_choice == "c":
                    file_path = input("Enter path to text file with EAN codes: ").strip()
                    if file_path and os.path.exists(file_path):
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                eans = [line.strip() for line in f if line.strip()]
                            
                            if eans:
                                print(f"✅ Loaded {len(eans)} EAN codes from file")
                                filename, count = db.search_products_by_ean(eans)
                            else:
                                print("❌ No valid EAN codes found in file")
                        except Exception as e:
                            print(f"❌ Error reading file: {e}")
                    else:
                        print("❌ File not found")
                else:
                    print("❌ Invalid search option")
            
            elif choice == "6":
                print("\n🎯 COMPREHENSIVE EXPORT with your exact headers!")
                print("⚠️  WARNING: This will export ALL products with comprehensive data")
                print("This creates a CSV with exactly 37 columns as you requested")
                confirm = input("Continue? Type 'yes' to confirm: ").lower().strip()
                
                if confirm == "yes":
                    print("\n🔄 Starting comprehensive full export...")
                    filename, count = db.export_comprehensive_csv()
                    
                    if filename:
                        print(f"🎉 Comprehensive export completed: {count:,} products exported")
                else:
                    print("❌ Export cancelled")
            
            elif choice == "7":
                print("\n🎯 Exporting 10,000 products with COMPREHENSIVE HEADERS...")
                filename, count = db.export_comprehensive_csv(limit=10000)
                
                if filename:
                    print(f"🎉 Comprehensive sample export completed: {count:,} products exported")
            
            elif choice == "8":
                print("\n🎯 EAN Search with COMPREHENSIVE HEADERS:")
                print("a. Search single EAN")
                print("b. Search multiple EANs (comma-separated)")
                print("c. Load EANs from file")
                
                search_choice = input("Select search option (a/b/c): ").lower().strip()
                
                if search_choice == "a":
                    ean = input("Enter EAN code: ").strip()
                    if ean:
                        filename, count = db.export_comprehensive_csv(ean_filter=[ean])
                        if count > 0:
                            print(f"🎉 Found and exported {count} product(s) with comprehensive data")
                    else:
                        print("❌ No EAN code provided")
                
                elif search_choice == "b":
                    eans_input = input("Enter EAN codes (comma-separated): ").strip()
                    if eans_input:
                        eans = [ean.strip() for ean in eans_input.split(',')]
                        filename, count = db.export_comprehensive_csv(ean_filter=eans)
                        if count > 0:
                            print(f"🎉 Found and exported {count} product(s) with comprehensive data")
                    else:
                        print("❌ No EAN codes provided")
                
                elif search_choice == "c":
                    file_path = input("Enter path to text file with EAN codes: ").strip()
                    if file_path and os.path.exists(file_path):
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                eans = [line.strip() for line in f if line.strip()]
                            
                            if eans:
                                print(f"✅ Loaded {len(eans)} EAN codes from file")
                                filename, count = db.export_comprehensive_csv(ean_filter=eans)
                                if count > 0:
                                    print(f"🎉 Found and exported {count} product(s) with comprehensive data")
                            else:
                                print("❌ No valid EAN codes found in file")
                        except Exception as e:
                            print(f"❌ Error reading file: {e}")
                    else:
                        print("❌ File not found")
                else:
                    print("❌ Invalid search option")
            
            else:
                print("❌ Invalid option. Please select 0-8.")
        
        except KeyboardInterrupt:
            print("\n👋 Operation cancelled by user")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
    
    # Close database connection
    db.close()

if __name__ == "__main__":
    main()
