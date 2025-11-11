from app import db
from app.models.user import User, UserRole
from app.models.category import Category
from app.models.product import Product
from app.models.order import Order, OrderLine, OrderStatus
from decimal import Decimal


def create_sample_data():
    """Créer des données de test pour l'application"""
    
    # Vérifier si les données existent déjà
    if User.query.first() or Category.query.first() or Product.query.first():
        print("Des données existent déjà dans la base. Suppression et recréation...")
        db.drop_all()
        db.create_all()
    
    print("Création des données de test...")
    
    # 1. Créer les utilisateurs
    print("Création des utilisateurs...")
    
    # Administrateur
    admin = User(
        email='admin@digimarket.com',
        first_name='Admin',
        last_name='DigiMarket',
        role=UserRole.ADMIN,
        address='123 Rue de l\'Administration, Paris, France',
        phone='+33123456789'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    
    # Clients
    clients_data = [
        {
            'email': 'jean.dupont@email.com',
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'address': '45 Avenue de la République, Lyon, France',
            'phone': '+33234567890'
        },
        {
            'email': 'marie.martin@email.com',
            'first_name': 'Marie',
            'last_name': 'Martin',
            'address': '78 Boulevard Saint-Michel, Marseille, France',
            'phone': '+33345678901'
        },
        {
            'email': 'pierre.bernard@email.com',
            'first_name': 'Pierre',
            'last_name': 'Bernard',
            'address': '12 Place de la Bastille, Paris, France',
            'phone': '+33456789012'
        }
    ]
    
    clients = []
    for client_data in clients_data:
        client = User(**client_data, role=UserRole.CLIENT)
        client.set_password('client123')
        db.session.add(client)
        clients.append(client)
    
    # 2. Créer les catégories
    print("Création des catégories...")
    
    categories_data = [
        {
            'name': 'Ordinateurs Portables',
            'description': 'Laptops et ultrabooks pour tous les usages'
        },
        {
            'name': 'Ordinateurs de Bureau',
            'description': 'PC de bureau et workstations'
        },
        {
            'name': 'Composants PC',
            'description': 'Processeurs, cartes mères, mémoire RAM, etc.'
        },
        {
            'name': 'Périphériques',
            'description': 'Claviers, souris, écrans, imprimantes'
        },
        {
            'name': 'Smartphones et Tablettes',
            'description': 'Appareils mobiles et accessoires'
        },
        {
            'name': 'Accessoires',
            'description': 'Câbles, housses, supports et autres accessoires'
        }
    ]
    
    categories = []
    for cat_data in categories_data:
        category = Category(**cat_data)
        db.session.add(category)
        categories.append(category)
    
    db.session.flush()  # Pour obtenir les IDs des catégories
    
    # 3. Créer les produits
    print("Création des produits...")
    
    products_data = [
        # Ordinateurs Portables
        {
            'name': 'MacBook Pro M2 13"',
            'description': 'MacBook Pro avec puce M2, 13 pouces, 8GB RAM, 256GB SSD',
            'price': Decimal('1299.99'),
            'stock_quantity': 15,
            'category_id': categories[0].id,
            'sku': 'MBP-M2-13-256'
        },
        {
            'name': 'Dell XPS 15',
            'description': 'Dell XPS 15, Intel i7, 16GB RAM, 512GB SSD, écran 4K',
            'price': Decimal('1599.99'),
            'stock_quantity': 8,
            'category_id': categories[0].id,
            'sku': 'DELL-XPS15-I7'
        },
        {
            'name': 'ASUS ROG Strix G15',
            'description': 'PC Gaming portable, AMD Ryzen 7, RTX 3060, 16GB RAM',
            'price': Decimal('1199.99'),
            'stock_quantity': 12,
            'category_id': categories[0].id,
            'sku': 'ASUS-ROG-G15'
        },
        
        # Ordinateurs de Bureau
        {
            'name': 'iMac M1 24"',
            'description': 'iMac avec puce M1, écran 24 pouces 4.5K, 8GB RAM, 256GB SSD',
            'price': Decimal('1399.99'),
            'stock_quantity': 10,
            'category_id': categories[1].id,
            'sku': 'IMAC-M1-24'
        },
        {
            'name': 'PC Gaming Custom RTX 4070',
            'description': 'PC Gaming assemblé, Intel i5-13400F, RTX 4070, 32GB RAM',
            'price': Decimal('1899.99'),
            'stock_quantity': 5,
            'category_id': categories[1].id,
            'sku': 'PC-GAMING-4070'
        },
        
        # Composants PC
        {
            'name': 'Intel Core i7-13700K',
            'description': 'Processeur Intel Core i7-13700K, 16 cœurs, 24 threads',
            'price': Decimal('399.99'),
            'stock_quantity': 25,
            'category_id': categories[2].id,
            'sku': 'INTEL-I7-13700K'
        },
        {
            'name': 'NVIDIA RTX 4080',
            'description': 'Carte graphique GeForce RTX 4080, 16GB GDDR6X',
            'price': Decimal('1199.99'),
            'stock_quantity': 7,
            'category_id': categories[2].id,
            'sku': 'RTX-4080-16GB'
        },
        {
            'name': 'Corsair Vengeance RGB Pro 32GB',
            'description': 'Kit mémoire DDR4-3200, 32GB (2x16GB), RGB',
            'price': Decimal('149.99'),
            'stock_quantity': 30,
            'category_id': categories[2].id,
            'sku': 'CORSAIR-32GB-RGB'
        },
        
        # Périphériques
        {
            'name': 'Logitech MX Master 3S',
            'description': 'Souris sans fil ergonomique pour la productivité',
            'price': Decimal('99.99'),
            'stock_quantity': 40,
            'category_id': categories[3].id,
            'sku': 'LOGI-MX-MASTER3S'
        },
        {
            'name': 'Keychron K2 V2',
            'description': 'Clavier mécanique sans fil, 75%, switches Gateron Blue',
            'price': Decimal('79.99'),
            'stock_quantity': 20,
            'category_id': categories[3].id,
            'sku': 'KEYCHRON-K2-V2'
        },
        {
            'name': 'LG 27UN850-W',
            'description': 'Écran 27" 4K USB-C, HDR400, 60Hz, IPS',
            'price': Decimal('349.99'),
            'stock_quantity': 15,
            'category_id': categories[3].id,
            'sku': 'LG-27UN850'
        },
        
        # Smartphones et Tablettes
        {
            'name': 'iPhone 15 Pro 256GB',
            'description': 'iPhone 15 Pro, 256GB, Titane Naturel',
            'price': Decimal('1199.99'),
            'stock_quantity': 18,
            'category_id': categories[4].id,
            'sku': 'IPHONE15-PRO-256'
        },
        {
            'name': 'Samsung Galaxy S24 Ultra',
            'description': 'Galaxy S24 Ultra, 512GB, S Pen inclus',
            'price': Decimal('1299.99'),
            'stock_quantity': 12,
            'category_id': categories[4].id,
            'sku': 'SAMSUNG-S24-ULTRA'
        },
        {
            'name': 'iPad Air M2 11"',
            'description': 'iPad Air avec puce M2, 11 pouces, 256GB, Wi-Fi',
            'price': Decimal('749.99'),
            'stock_quantity': 22,
            'category_id': categories[4].id,
            'sku': 'IPAD-AIR-M2-11'
        },
        
        # Accessoires
        {
            'name': 'Câble USB-C vers USB-C 2m',
            'description': 'Câble USB-C de charge rapide, 2 mètres, 100W',
            'price': Decimal('24.99'),
            'stock_quantity': 100,
            'category_id': categories[5].id,
            'sku': 'CABLE-USBC-2M'
        },
        {
            'name': 'Support Laptop Ergonomique',
            'description': 'Support réglable en aluminium pour ordinateurs portables',
            'price': Decimal('39.99'),
            'stock_quantity': 35,
            'category_id': categories[5].id,
            'sku': 'SUPPORT-LAPTOP-ALU'
        }
    ]
    
    products = []
    for product_data in products_data:
        product = Product(**product_data)
        db.session.add(product)
        products.append(product)
    
    db.session.flush()  # Pour obtenir les IDs des produits
    
    # 4. Créer quelques commandes d'exemple
    print("Création des commandes d'exemple...")
    
    # Commande 1 - Jean Dupont
    order1 = Order(
        user_id=clients[0].id,
        shipping_address=clients[0].address,
        status=OrderStatus.DELIVERED
    )
    db.session.add(order1)
    db.session.flush()
    
    # Lignes de la commande 1
    order1_lines = [
        OrderLine(
            order_id=order1.id,
            product_id=products[0].id,  # MacBook Pro
            quantity=1,
            unit_price=products[0].price
        ),
        OrderLine(
            order_id=order1.id,
            product_id=products[8].id,  # Souris Logitech
            quantity=1,
            unit_price=products[8].price
        )
    ]
    
    for line in order1_lines:
        db.session.add(line)
    
    order1.calculate_total()
    
    # Commande 2 - Marie Martin
    order2 = Order(
        user_id=clients[1].id,
        shipping_address=clients[1].address,
        status=OrderStatus.SHIPPED
    )
    db.session.add(order2)
    db.session.flush()
    
    # Lignes de la commande 2
    order2_lines = [
        OrderLine(
            order_id=order2.id,
            product_id=products[4].id,  # PC Gaming
            quantity=1,
            unit_price=products[4].price
        ),
        OrderLine(
            order_id=order2.id,
            product_id=products[9].id,  # Clavier Keychron
            quantity=1,
            unit_price=products[9].price
        ),
        OrderLine(
            order_id=order2.id,
            product_id=products[10].id,  # Écran LG
            quantity=1,
            unit_price=products[10].price
        )
    ]
    
    for line in order2_lines:
        db.session.add(line)
    
    order2.calculate_total()
    
    # Commande 3 - Pierre Bernard (en attente)
    order3 = Order(
        user_id=clients[2].id,
        shipping_address=clients[2].address,
        status=OrderStatus.PENDING
    )
    db.session.add(order3)
    db.session.flush()
    
    # Lignes de la commande 3
    order3_lines = [
        OrderLine(
            order_id=order3.id,
            product_id=products[11].id,  # iPhone 15 Pro
            quantity=1,
            unit_price=products[11].price
        ),
        OrderLine(
            order_id=order3.id,
            product_id=products[14].id,  # Câble USB-C
            quantity=2,
            unit_price=products[14].price
        )
    ]
    
    for line in order3_lines:
        db.session.add(line)
    
    order3.calculate_total()
    
    # Valider toutes les modifications
    db.session.commit()
    
    print("✅ Données de test créées avec succès!")
    print("\n📊 Résumé des données créées:")
    print(f"   - {User.query.count()} utilisateurs (1 admin, {User.query.filter_by(role=UserRole.CLIENT).count()} clients)")
    print(f"   - {Category.query.count()} catégories")
    print(f"   - {Product.query.count()} produits")
    print(f"   - {Order.query.count()} commandes")
    print(f"   - {OrderLine.query.count()} lignes de commande")
    print("\n🔐 Comptes de test:")
    print("   Admin: admin@digimarket.com / admin123")
    print("   Client 1: jean.dupont@email.com / client123")
    print("   Client 2: marie.martin@email.com / client123")
    print("   Client 3: pierre.bernard@email.com / client123")