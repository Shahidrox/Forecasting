# The code you provided is an excerpt from a Python file named seeds.py. It contains two lists: USERS_LIST and PRODUCT_LIST.
# The USERS_LIST is a list of dictionaries, where each dictionary represents a user. Each user dictionary has three key-value pairs: 'username', 'email', and 'password'. This list is used to store user information, such as their username, email, and password.
# The PRODUCT_LIST is also a list of dictionaries, where each dictionary represents a product. Each product dictionary has several key-value pairs, including 'name', 'brand', 'price', 'rating', 'category', 'slug', and 'image'. These key-value pairs store information about the product, such as its name, brand, price, rating, category, slug (a unique identifier), and image path. This list is used to store information about various products.
# Both lists are defined as global variables, which means they can be accessed and modified from anywhere within the code.
# It's important to note that the code you provided is just a snippet, and there may be more code in the seeds.py file that utilizes these lists.

USERS_LIST = [
    { 'username': 'Test1', 'email': 'test1@gmail.com', 'password': 'password'},
    { 'username': 'Test2', 'email': 'test2@gmail.com', 'password': 'password'},
    { 'username': 'Test3', 'email': 'test2@gmail.com', 'password': 'password'}
]

PRODUCT_LIST = [
    {"name": "Rose Essential Gift Box", "brand": "Kama Ayurveda", "price": 2000, "rating": 4.5, "category": "Skincare", "slug": "rose-essential-gift-box", 'image': "assets/images/products/rose-essential-gift-box.png"},
    {"name": "9 to 5 Primer + Matte Powder Foundation Compact", "brand": "Lakme", "price": 600, "rating": 4.3, "category": "Makeup", "slug": "9-to-5-primer-matte-powder-foundation-compact", "image": "assets/images/products/9-to-5-primer-matte-powder-foundation-compact.png"},
    {"name": "Velvet Matte Lipstick", "brand": "Colorbar", "price": 300, "rating": 4.2, "category": "Makeup", "slug": "velvet-matte-lipstick", "image": "assets/images/products/velvet-matte-lipstick.png"},
    {"name": "Safe Sun 3-In-1 Matte Look Daily Sunblock SPF-40", "brand": "Lotus Herbals", "price": 300, "rating": 4.1, "category": "Skincare", "slug": "safe-sun-3-in-1-matte-look-daily-sunblock-spf-40", "image": "assets/images/products/safe-sun-3-in-1-matte-look-daily-sunblock-spf-40.png"},
    {"name": "Ultime Pro HD Intense Matte Lips + Primer", "brand": "Faces Canada", "price": 600, "rating": 4.0, "category": "Makeup", "slug": "ultime-pro-hd-intense-matte-lips-primer", "image": "assets/images/products/ultime-pro-hd-intense-matte-lips-primer.png"},
    {"name": "Infallible Pro-Matte Liquid Lipstick", "brand": "L'Oreal Paris", "price": 800, "rating": 4.0, "category": "Makeup", "slug": "infallible-pro-matte-liquid-lipstick", "image": "assets/images/products/infallible-pro-matte-liquid-lipstick.png"},
    {"name": "Fit Me Matte + Poreless Foundation", "brand": "Maybelline", "price": 500, "rating": 4.0, "category": "Makeup", "slug": "fit-me-matte-poreless-foundation", "image": "assets/images/products/fit-me-matte-poreless-foundation.png"},
    {"name": "Smudge Me Not Liquid Lipstick", "brand": "Sugar Cosmetics", "price": 500, "rating": 4.0, "category": "Makeup", "slug": "smudge-me-not-liquid-lipstick", "image": "assets/images/products/smudge-me-not-liquid-lipstick.png"},
    {"name": "Soundarya Radiance Cream With 24K Gold", "brand": "Forest Essentials", "price": 4000, "rating": 4.0, "category": "Skincare", "slug": "soundarya-radiance-cream-with-24k-gold", "image": "assets/images/products/soundarya-radiance-cream-with-24k-gold.png"},
    {"name": "Purifying Neem Face Wash", "brand": "Himalaya", "price": 150, "rating": 4.0, "category": "Skincare", "slug": "purifying-neem-face-wash", "image": "assets/images/products/purifying-neem-face-wash.png"},
    {"name": "Bio Papaya Revitalizing Tan-Removal Scrub", "brand": "Biotique", "price": 200, "rating": 4.0, "category": "Skincare", "slug": "bio-papaya-revitalizing-tan-removal-scrub", "image": "assets/images/products/bio-papaya-revitalizing-tan-removal-scrub.png"},
]