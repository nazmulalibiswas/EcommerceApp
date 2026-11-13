import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'

import django
django.setup()

from django.db import connection
from store.models import Products, Users, Orders, OrderItems, Categories, Payments, Reviews

cursor = connection.cursor()

model_table_map = {
    'users': Users,
    'products': Products,
    'orders': Orders,
    'order_items': OrderItems,
    'categories': Categories,
    'payments': Payments,
    'reviews': Reviews,
}

print('=' * 70)
print('  DB COLUMNS vs DJANGO MODEL FIELDS - COMPARISON')
print('=' * 70)

for table_name, model in model_table_map.items():
    # Get DB columns
    cursor.execute(
        'SELECT column_name, is_nullable FROM information_schema.columns '
        'WHERE table_name = %s AND table_schema = %s ORDER BY ordinal_position',
        [table_name, 'public']
    )
    db_cols = {row[0]: row[1] for row in cursor.fetchall()}

    # Get Django model fields (column names)
    django_fields = {}
    for f in model._meta.get_fields():
        if hasattr(f, 'column'):
            django_fields[f.column] = f.name

    # Compare
    in_both = set(db_cols.keys()) & set(django_fields.keys())
    only_in_db = set(db_cols.keys()) - set(django_fields.keys())
    only_in_django = set(django_fields.keys()) - set(db_cols.keys())

    print(f'\n--- {table_name.upper()} (Model: {model.__name__}) ---')
    print(f'  DB columns: {len(db_cols)} | Django fields: {len(django_fields)}')
    print()

    if in_both:
        print(f'  MATCHED ({len(in_both)}):')
        for col in sorted(in_both):
            print(f'    [OK] {col}')

    if only_in_db:
        print(f'\n  ONLY IN DB - NOT IN DJANGO MODEL ({len(only_in_db)}):')
        for col in sorted(only_in_db):
            nullable = db_cols[col]
            status = 'SAFE (nullable)' if nullable == 'YES' else 'WARNING (NOT NULL)'
            print(f'    [!!] {col}  --> {status}')

    if only_in_django:
        print(f'\n  ONLY IN DJANGO - NOT IN DB ({len(only_in_django)}):')
        for col in sorted(only_in_django):
            print(f'    [XX] {col}  --> PROBLEM! Will crash on query!')

    if not only_in_db and not only_in_django:
        print('  >>> PERFECT MATCH!')

# Test actual CRUD operations
print('\n' + '=' * 70)
print('  CRUD OPERATION TEST')
print('=' * 70)

# Test READ
try:
    list(Users.objects.all()[:1])
    print('  [OK] Users READ works')
except Exception as e:
    print(f'  [FAIL] Users READ: {e}')

try:
    list(Products.objects.all()[:1])
    print('  [OK] Products READ works')
except Exception as e:
    print(f'  [FAIL] Products READ: {e}')

try:
    list(Orders.objects.all()[:1])
    print('  [OK] Orders READ works')
except Exception as e:
    print(f'  [FAIL] Orders READ: {e}')

try:
    list(OrderItems.objects.all()[:1])
    print('  [OK] OrderItems READ works')
except Exception as e:
    print(f'  [FAIL] OrderItems READ: {e}')

try:
    list(Categories.objects.all()[:1])
    print('  [OK] Categories READ works')
except Exception as e:
    print(f'  [FAIL] Categories READ: {e}')

try:
    list(Payments.objects.all()[:1])
    print('  [OK] Payments READ works')
except Exception as e:
    print(f'  [FAIL] Payments READ: {e}')

try:
    list(Reviews.objects.all()[:1])
    print('  [OK] Reviews READ works')
except Exception as e:
    print(f'  [FAIL] Reviews READ: {e}')

print('\n' + '=' * 70)
print('  DONE')
print('=' * 70)
