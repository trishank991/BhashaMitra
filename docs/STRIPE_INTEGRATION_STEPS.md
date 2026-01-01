# BhashaMitra Stripe Integration Guide

## Step-by-Step Instructions to Enable Stripe Payments

### Prerequisites
You have already provided in `.env`:
- ✅ `STRIPE_PUBLISHABLE_KEY`
- ✅ `STRIPE_SECRET_KEY`

---

### Step 1: Complete Backend Configuration

Your backend `.env` file needs these Stripe variables:

```bash
# Add to bhashamitra-backend/.env

# Stripe Price IDs (create these in Stripe Dashboard)
STRIPE_PRICE_STANDARD_MONTHLY=price_xxxxxxxxxxxxxx
STRIPE_PRICE_STANDARD_YEARLY=price_xxxxxxxxxxxxxx

# Premium is optional - enable only when live classes are ready
STRIPE_PRICE_PREMIUM_MONTHLY=price_xxxxxxxxxxxxxx  # Optional
STRIPE_PRICE_PREMIUM_YEARLY=price_xxxxxxxxxxxxxx  # Optional

# Frontend URL (for Stripe callbacks)
FRONTEND_URL=http://localhost:3000
```

**Important:** Premium tier is disabled by default. It will only show on the pricing page if `ENABLE_PREMIUM_TIER=true` is set. In development mode (`DJANGO_ENV=dev`), Premium is always available for testing.

---

### Step 2: Create Products in Stripe Dashboard

1. Go to [Stripe Dashboard](https://dashboard.stripe.com/products)
2. Create products:

#### Product 1: STANDARD (Required)
- **Name:** "BhashaMitra Standard"
- **Description:** "Perfect for individual learners" (optional)
- **Pricing:**
  - Monthly: Create price → Recurring → Monthly → Enter amount (e.g., 20 NZD)
  - Yearly: Create price → Recurring → Yearly → Enter amount (e.g., 200 NZD)
- Copy the price IDs (they start with `price_`)

#### Product 2: PREMIUM (Optional - Launch Later)
- **Name:** "BhashaMitra Premium"
- **Description:** "Family plan with live classes" (optional)
- **Pricing:**
  - Monthly: Create price → Recurring → Monthly → Enter amount (e.g., 30 NZD)
  - Yearly: Create price → Recurring → Yearly → Enter amount (e.g., 300 NZD)
- Copy the price IDs

---

### Step 3: Update Backend .env with Price IDs

Edit `bhashamitra-backend/.env`:

```bash
# Required - Standard tier
STRIPE_PRICE_STANDARD_MONTHLY=price_standard_monthly_id
STRIPE_PRICE_STANDARD_YEARLY=price_standard_yearly_id

# Optional - Premium tier (uncomment when ready to launch Premium)
# STRIPE_PRICE_PREMIUM_MONTHLY=price_premium_monthly_id
# STRIPE_PRICE_PREMIUM_YEARLY=price_premium_yearly_id
# ENABLE_PREMIUM_TIER=true
```

---

### Step 4: Launch Strategy - Standard Only (Recommended for MVP)

For MVP launch, only configure Standard tier:

```bash
# .env for MVP launch
STRIPE_PRICE_STANDARD_MONTHLY=price_xxx
STRIPE_PRICE_STANDARD_YEARLY=price_xxx
# Leave Premium price IDs empty or commented out
```

**Result:**
- Pricing page shows: Free and Standard plans
- Premium is hidden until enabled
- Development mode: You can still test Premium features for yourself

### Step 5: Enable Premium Later

When live classes are ready, uncomment the Premium variables:

```bash
STRIPE_PRICE_PREMIUM_MONTHLY=price_xxx
STRIPE_PRICE_PREMIUM_YEARLY=price_xxx
ENABLE_PREMIUM_TIER=true
```

---

### Step 6: Configure Frontend (Optional)

The frontend pricing page reads from the backend API, so no frontend config is needed.

---

### Step 7: Test the Integration

#### Local Development Testing

1. **Start the backend:**
   ```bash
   cd bhashamitra-backend
   python manage.py runserver
   ```

2. **Start the frontend:**
   ```bash
   cd bhashamitra-frontend
   npm run dev
   ```

3. **Test the flow:**
   - Register a new account
   - Go to `/pricing`
   - Click "Get Started" on any plan
   - You should be redirected to Stripe Checkout
   - Use test card: `4242 4242 4242 4242` (any future date, any CVC)

#### Test Cards (Stripe Test Mode)

| Card Number | Description |
|-------------|-------------|
| 4242 4242 4242 4242 | Successful payment |
| 4000 0000 0000 9995 | Declined payment |
| 4000 0000 0000 3220 | 3D Secure required |

---

### Step 8: Set Up Webhooks (Production Only)

For production, you need to configure webhooks so Stripe can notify your backend of subscription events.

#### How to Get Webhook Secret:

1. **Go to Stripe Dashboard:**
   - Navigate to [Stripe Webhooks](https://dashboard.stripe.com/webhooks)

2. **Add Endpoint:**
   - Click "Add an endpoint"
   - Endpoint URL: `https://yourdomain.com/api/v1/payments/webhooks/stripe/`
     - For testing locally: Use Stripe CLI (see below)

3. **Select Events to Listen:**
   - Click "Select events"
   - Search and select:
     - ✅ `checkout.session.completed`
     - ✅ `customer.subscription.created`
     - ✅ `customer.subscription.updated`
     - ✅ `customer.subscription.deleted`
     - ✅ `invoice.paid`
     - ✅ `invoice.payment_failed`
   - Click "Add events"

4. **Get Webhook Secret:**
   - After creating the webhook, scroll down to "Signing secret"
   - Click "Reveal" next to "secret"
   - Copy the secret (starts with `whsec_`)
   - Add to `.env`:
     ```bash
     STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxxx
     ```

#### Testing Webhooks Locally (Stripe CLI)

For local development, use Stripe CLI to forward webhooks:

1. **Install Stripe CLI:**
   - [Download here](https://stripe.com/docs/stripe-cli#install)

2. **Login to Stripe:**
   ```bash
   stripe login
   ```

3. **Forward webhooks to your local server:**
   ```bash
   stripe listen --forward-to localhost:8000/api/v1/payments/webhooks/stripe/
   ```

4. **Copy the webhook secret** shown by the CLI (starts with `whsec_`)

5. **Use the CLI secret** in your `.env` for local testing

---

### Step 9: Switch to Production Mode

When ready to go live:

1. **Get live API keys:**
   - Go to Stripe Dashboard → Developers → API keys
   - Switch from "Test mode" to "Live mode"
   - Copy live publishable and secret keys

2. **Update backend .env:**
   ```bash
   STRIPE_PUBLISHABLE_KEY=pk_live_xxxxxxxxxxxxxx
   STRIPE_SECRET_KEY=sk_live_xxxxxxxxxxxxxx
   STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxxx
   ```

3. **Create live price IDs:**
   - Repeat Step 2 in live mode
   - Update price ID env variables

4. **Update environment:**
   ```bash
   DJANGO_ENV=prod
   DEBUG=False
   FRONTEND_URL=https://yourdomain.com
   ```

---

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/payments/pricing/` | GET | Get pricing info (public) |
| `/api/v1/payments/checkout/` | POST | Create checkout session |
| `/api/v1/payments/subscription/` | GET | Get current subscription |
| `/api/v1/payments/portal/` | POST | Open customer portal |
| `/api/v1/payments/history/` | GET | Get payment history |
| `/api/v1/payments/webhooks/stripe/` | POST | Stripe webhook handler |

---

### Tier Availability Logic

| Environment | Standard | Premium |
|-------------|----------|---------|
| Development (`dev`) | ✅ Available | ✅ Always available |
| Production | ✅ Available | ⚠️ Only if `ENABLE_PREMIUM_TIER=true` |

This allows you to:
1. Launch MVP with Standard only
2. Test Premium features in development
3. Enable Premium later when ready

---

### Troubleshooting

#### "Price ID not configured" error
- Make sure you created products and prices in Stripe Dashboard
- Verify price IDs are correctly set in `.env`

#### Checkout redirects to pricing with `canceled=true`
- Check backend logs for error details
- Common cause: User already has an active subscription

#### Webhook errors
- Verify webhook URL is accessible from the internet
- Check webhook signature verification
- Ensure `STRIPE_WEBHOOK_SECRET` is set correctly

---

### Next Steps

1. Add the missing Stripe variables to your `.env` file
2. Create products and prices in Stripe Dashboard
3. Test the checkout flow locally
4. Configure webhooks for production
