# 🚀 Deployment Guide

## Vercel Deployment Checklist

### ✅ Pre-Deployment Checklist

- [ ] **API Keys Ready**
  - [ ] Replicate API token from [replicate.com/account/api-tokens](https://replicate.com/account/api-tokens)
  - [ ] OpenAI API key from [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

- [ ] **Code Ready**
  - [ ] All changes committed to GitHub
  - [ ] `.env` file NOT committed (should be in `.gitignore`)
  - [ ] `requirements.txt` includes all dependencies

### 🔧 Vercel Configuration

#### 1. Environment Variables (Required)

Set these in your Vercel project dashboard:

```env
REPLICATE_API_TOKEN=r8_your_actual_replicate_token_here
OPENAI_API_KEY=sk-your_actual_openai_key_here
VIDEO_PROVIDER=replicate
REPLICATE_MODEL=pixverse/pixverse-v5
APP_ORIGIN=*
```

#### 2. Build Settings

Vercel should auto-detect these settings:
- **Framework Preset**: Other
- **Build Command**: (leave empty)
- **Output Directory**: (leave empty)
- **Install Command**: `pip install -r requirements.txt`

#### 3. Function Configuration

The `vercel.json` is configured with:
- **Max Duration**: 300 seconds (5 minutes) for video generation
- **Max Lambda Size**: 50MB for AI dependencies
- **Python Runtime**: Latest supported version

### 🧪 Testing Deployment

After deployment, test these features:

1. **Basic App Load**
   - [ ] Homepage loads correctly
   - [ ] No console errors

2. **Prompt Optimization**
   - [ ] Enter a test prompt
   - [ ] Click "Optimize Prompt"
   - [ ] Should return optimized text (not mock response)

3. **Video Generation**
   - [ ] Enter a test prompt (e.g., "A cat walking")
   - [ ] Click "Generate Video"
   - [ ] Should show "processing" status
   - [ ] Wait 2-3 minutes for completion
   - [ ] Video should be playable

### 🐛 Common Issues & Solutions

#### Issue: "No REPLICATE_API_TOKEN found"
**Solution**: Check environment variables in Vercel dashboard

#### Issue: Video generation fails with 404
**Solution**: Verify `REPLICATE_MODEL` is set to `pixverse/pixverse-v5`

#### Issue: Prompt optimization shows mock response
**Solution**: Verify `OPENAI_API_KEY` is correctly set

#### Issue: Function timeout
**Solution**: Video generation can take 2-5 minutes, this is normal

#### Issue: CORS errors
**Solution**: Ensure `APP_ORIGIN=*` is set in environment variables

### 📊 Performance Notes

- **Cold Start**: First request may take 10-15 seconds
- **Video Generation**: 2-5 minutes depending on complexity
- **Prompt Optimization**: 1-3 seconds
- **Caching**: Identical prompts return cached results instantly

### 🔒 Security Notes

- API keys are stored securely in Vercel environment variables
- No sensitive data is logged or exposed in client-side code
- CORS is configured for security while allowing necessary access

### 📈 Monitoring

Monitor your deployment:
- **Vercel Dashboard**: Function logs and performance
- **Replicate Dashboard**: API usage and costs
- **OpenAI Dashboard**: API usage and costs