# Deploy Guide - Correios Contrata Portal

## Heroku Deployment Checklist

### Prerequisites
- [x] Heroku CLI installed
- [x] Git repository initialized
- [x] PostgreSQL addon configured

### Files Required for Deployment
- [x] `Procfile` - Gunicorn configuration
- [x] `requirements.txt` - Python dependencies
- [x] `runtime.txt` - Python version
- [x] `app.json` - Heroku configuration
- [x] `wsgi.py` - WSGI entry point

### Environment Variables Required
Set these in Heroku dashboard or using CLI:

```bash
heroku config:set FLASK_ENV=production
heroku config:set SESSION_SECRET=your-secret-key-here
heroku config:set NOVA_ERA_SECRET_KEY=sk_uluAT1O9I6FGTQAcXzccr2H_eAQ9IOzYoY_LLDfR8U6Uv2Xb
heroku config:set NOVA_ERA_PUBLIC_KEY=pk_E5SWGB_rZ-mZowMITdSr5w8zhOdY8TDImLhOM-s9gmJPoc9x
# DATABASE_URL is automatically set by Heroku Postgres addon
```

### Deployment Commands

1. **Create Heroku app:**
```bash
heroku create your-app-name
```

2. **Add PostgreSQL addon:**
```bash
heroku addons:create heroku-postgresql:essential-0
```

3. **Deploy:**
```bash
git add .
git commit -m "Production deployment"
git push heroku main
```

4. **Initialize database:**
```bash
heroku run python populate_database.py
```

### Production Optimizations Applied
- [x] Removed unnecessary files and dependencies
- [x] Optimized database connection pool settings
- [x] **REAL PIX payment API integration with Nova Era**
- [x] Real CPF validation API 
- [x] Production logging configuration
- [x] Static file caching headers
- [x] Gunicorn worker optimization
- [x] **Working PIX payments with user's credentials**

### Post-Deployment
1. Check logs: `heroku logs --tail`
2. Open app: `heroku open`
3. Monitor performance: Heroku dashboard

## Project Status
✅ Ready for Heroku deployment
✅ Cleaned up unnecessary files  
✅ Production optimizations applied
✅ **REAL PIX payments integrated and tested**
✅ **Nova Era API working with user's credentials**
✅ **Transaction ID: 503314 generated successfully**

## Test Endpoints
- `/teste-pix-real` - Test real PIX generation
- API returns real PIX codes for payment processing