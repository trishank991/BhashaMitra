-- SQL Script to seed test users directly on PostgreSQL database
-- Run this on the Render production database
-- Connection: Use Render's DATABASE_URL or connect via psql

-- Note: This script uses the users_user table from the custom User model
-- The table name includes the app prefix: auth_user vs users_user

-- First, let's check if we're using the custom User model or auth.User
-- Assuming the custom User model in apps.users

-- Insert FREE tier test user
INSERT INTO users_user (
    password,
    last_login,
    is_superuser,
    username,
    first_name,
    last_name,
    email,
    is_staff,
    is_active,
    date_joined,
    name,
    role,
    avatar_url,
    subscription_tier,
    subscription_expires_at,
    email_verified,
    email_verified_at,
    is_onboarded,
    onboarding_completed_at,
    tts_provider,
    preferred_language,
    story_limit
) VALUES (
    'pbkdf2_sha256$720000$test$hashed_password_placeholder',  -- Will be replaced with proper hash
    NULL,
    FALSE,
    'freetest',
    '',
    '',
    'free@test.com',
    FALSE,
    TRUE,
    NOW() AT TIME ZONE 'UTC',
    'Free Test Parent',
    'parent',
    NULL,
    'FREE',
    NULL,
    TRUE,
    NOW() AT TIME ZONE 'UTC',
    TRUE,
    NOW() AT TIME ZONE 'UTC',
    'edge',
    'HINDI',
    5
) ON CONFLICT (email) DO UPDATE SET
    name = EXCLUDED.name,
    subscription_tier = EXCLUDED.subscription_tier,
    subscription_expires_at = EXCLUDED.subscription_expires_at,
    email_verified = EXCLUDED.email_verified,
    email_verified_at = EXCLUDED.email_verified_at,
    is_onboarded = EXCLUDED.is_onboarded,
    onboarding_completed_at = EXCLUDED.onboarding_completed_at;

-- Insert STANDARD tier test user
INSERT INTO users_user (
    password,
    last_login,
    is_superuser,
    username,
    first_name,
    last_name,
    email,
    is_staff,
    is_active,
    date_joined,
    name,
    role,
    avatar_url,
    subscription_tier,
    subscription_expires_at,
    email_verified,
    email_verified_at,
    is_onboarded,
    onboarding_completed_at,
    tts_provider,
    preferred_language,
    story_limit
) VALUES (
    'pbkdf2_sha256$720000$test$hashed_password_placeholder',
    NULL,
    FALSE,
    'standardtest',
    '',
    '',
    'standard@test.com',
    FALSE,
    TRUE,
    NOW() AT TIME ZONE 'UTC',
    'Standard Test Parent',
    'parent',
    NULL,
    'STANDARD',
    NOW() AT TIME ZONE 'UTC' + INTERVAL '30 days',
    TRUE,
    NOW() AT TIME ZONE 'UTC',
    TRUE,
    NOW() AT TIME ZONE 'UTC',
    'openai',
    'HINDI',
    -1  -- Unlimited
) ON CONFLICT (email) DO UPDATE SET
    name = EXCLUDED.name,
    subscription_tier = EXCLUDED.subscription_tier,
    subscription_expires_at = EXCLUDED.subscription_expires_at,
    email_verified = EXCLUDED.email_verified,
    email_verified_at = EXCLUDED.email_verified_at,
    is_onboarded = EXCLUDED.is_onboarded,
    onboarding_completed_at = EXCLUDED.onboarding_completed_at;

-- Insert PREMIUM tier test user
INSERT INTO users_user (
    password,
    last_login,
    is_superuser,
    username,
    first_name,
    last_name,
    email,
    is_staff,
    is_active,
    date_joined,
    name,
    role,
    avatar_url,
    subscription_tier,
    subscription_expires_at,
    email_verified,
    email_verified_at,
    is_onboarded,
    onboarding_completed_at,
    tts_provider,
    preferred_language,
    story_limit
) VALUES (
    'pbkdf2_sha256$720000$test$hashed_password_placeholder',
    NULL,
    FALSE,
    'premiumtest',
    '',
    '',
    'premium@test.com',
    FALSE,
    TRUE,
    NOW() AT TIME ZONE 'UTC',
    'Premium Test Parent',
    'parent',
    NULL,
    'PREMIUM',
    NOW() AT TIME ZONE 'UTC' + INTERVAL '30 days',
    TRUE,
    NOW() AT TIME ZONE 'UTC',
    TRUE,
    NOW() AT TIME ZONE 'UTC',
    'google',
    'HINDI',
    -1  -- Unlimited
) ON CONFLICT (email) DO UPDATE SET
    name = EXCLUDED.name,
    subscription_tier = EXCLUDED.subscription_tier,
    subscription_expires_at = EXCLUDED.subscription_expires_at,
    email_verified = EXCLUDED.email_verified,
    email_verified_at = EXCLUDED.email_verified_at,
    is_onboarded = EXCLUDED.is_onboarded,
    onboarding_completed_at = EXCLUDED.onboarding_completed_at;

-- Note: The password field needs to be set using Django's password hashing
-- Run the Django management command via Render CLI or shell
