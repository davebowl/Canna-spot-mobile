# DNS Configuration for cheapdomains.lol → Koyeb

## Problem
CNAME records cannot be used for root domains (@) with most DNS providers.

## Solution: Use A Records

### Step 1: Find Koyeb's IP Address
Run this command to get the IP:
```bash
nslookup c4a13e5a-6099-442d-a0d9-cbef95a75856.cname.koyeb.app
```

### Step 2: Update DNS Records

In your DNS control panel (my-control-panel.com), set:

```dns
# For root domain - use A record with Koyeb's IP
@                3600  IN  A      <koyeb-ip-from-step-1>

# For www subdomain - use CNAME
www              3600  IN  CNAME  c4a13e5a-6099-442d-a0d9-cbef95a75856.cname.koyeb.app.
```

### Step 3: In Koyeb Dashboard

1. Go to your service → Settings → Domains
2. Remove the failing `cheepdomains.lol` domain
3. Add two domains separately:
   - `cheapdomains.lol` (root)
   - `www.cheapdomains.lol` (subdomain)

## Alternative: Use WWW as Primary

If you want to avoid IP address issues:

```dns
# Root redirects to www (A record to your host)
@                3600  IN  A      198.251.81.49

# WWW points to Koyeb
www              3600  IN  CNAME  c4a13e5a-6099-442d-a0d9-cbef95a75856.cname.koyeb.app.
```

Then set up a redirect on your web host:
- Redirect `cheapdomains.lol` → `www.cheapdomains.lol`

Only add `www.cheapdomains.lol` in Koyeb.

## Note
I noticed the typo: Koyeb shows `cheepdomains.lol` but your domain is `cheapdomains.lol`. 
Make sure you're adding the correct spelling!
