#!/usr/bin/env python3
"""
Generate Django password hashes for test users.
This script creates the proper password hashes that can be used in SQL or directly.

Run this locally to generate hashes, then apply them to production.
"""

import hashlib
import os
import sys

# Add Django to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')

import django
django.setup()

from django.contrib.auth.hashers import make_password

def generate_test_user_hashes():
    """Generate password hashes for test users."""
    
    password = 'test1234'
    
    test_users = [
        {'email': 'free@test.com', 'tier': 'FREE'},
        {'email': 'standard@test.com', 'tier': 'STANDARD'},
        {'email': 'premium@test.com', 'tier': 'PREMIUM'},
    ]
    
    print("=" * 60)
    print("Django Password Hashes for Test Users")
    print("Password for all users: test1234")
    print("=" * 60)
    
    for user in test_users:
        email = user['email']
        tier = user['tier']
        
        # Generate the hash
        password_hash = make_password(password)
        
        print(f"\n{tier} Tier User: {email}")
        print(f"  Email: {email}")
        print(f"  Password: {password}")
        print(f"  Password Hash:")
        print(f"    {password_hash}")
        print()
        
        # Save to file for reference
        with open('test_user_hashes.txt', 'a') as f:
            f.write(f"{email},{password},{password_hash}\n")
    
    print("=" * 60)
    print("Hashes saved to test_user_hashes.txt")

if __name__ == '__main__':
    generate_test_user_hashes()
