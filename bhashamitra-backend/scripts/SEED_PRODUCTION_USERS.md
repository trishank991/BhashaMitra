# Seed Test Users on Production Database

## Root Cause

The test users were seeded on your **local development database**, but the production website at `https://bhasha-mitra.vercel.app` uses the **Render backend** at `https://bhashamitra.onrender.com/api/v1`.

## Solution: Use the New API Endpoint

I've added a temporary endpoint to seed users directly on production. Run this command:

```bash
curl -X POST https://bhashamitra.onrender.com/api/v1/users/seed-test-users/ \
  -H "Content-Type: application/json" \
  -H "X-Seed-Secret: dev-seed-secret-change-in-prod"
```

This will create/update the three test users with proper password hashing.

## Expected Response

```json
{
  "success": true,
  "message": "Successfully seeded 3 test users",
  "users": {
    "free@test.com": "test1234",
    "standard@test.com": "test1234",
    "premium@test.com": "test1234"
  },
  "created": 3,
  "updated": 0
}
```

## Test Credentials

After running the seed command, use these credentials on https://bhasha-mitra.vercel.app:

| Tier     | Email             | Password  |
|----------|-------------------|-----------|
| FREE     | free@test.com     | test1234  |
| STANDARD | standard@test.com | test1234  |
| PREMIUM  | premium@test.com  | test1234  |

## Security Note

⚠️ **Important**: After seeding, please:
1. Remove the `seed-test-users` endpoint from `apps/users/urls.py` and `apps/users/views.py`
2. Or set a strong `SEED_USERS_SECRET` environment variable on Render

## Alternative: Manual Shell Access

If the API approach doesn't work:

1. Go to Render Dashboard > Services > bhashamitra-backend > Shell
2. Run:
   ```bash
   python manage.py seed_test_users
   ```
3. Then reset passwords:
   ```bash
   python manage.py shell -c "
   from django.contrib.auth.models import User
   for email in ['free@test.com', 'standard@test.com', 'premium@test.com']:
       u = User.objects.get(email=email)
       u.set_password('test1234')
       u.save()
       print(f'Password reset for {email}')
   "
   ```

## Files Modified

- [`apps/users/views.py`](apps/users/views.py) - Added `SeedTestUsersView` class
- [`apps/users/urls.py`](apps/users/urls.py) - Added `/api/v1/users/seed-test-users/` route
