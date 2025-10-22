# 🚀 Crypto Compatibility Engine

**AI-Powered Crypto Dating for Farcaster** - Find your crypto soulmate based on wallet behavior, NFT taste, and DeFi strategies!

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/crypto-compatibility-engine)

## ✨ Features

🎯 **Smart Personality Analysis**
- Analyzes crypto behavior patterns
- 10+ unique personality types (Bitcoin Maxi, DeFi Degen, NFT Collector, etc.)
- AI-powered comedy generation

💕 **Intelligent Matching Algorithm**
- Token preferences (30%)
- Risk tolerance (25%)
- NFT taste (20%)
- Social behavior (15%)
- Community engagement (10%)

🎭 **Viral Content Generation**
- Funny compatibility reports
- Shareable results
- Date suggestions based on crypto interests
- Meme-worthy output

📱 **Farcaster Mini App**
- Interactive frames
- One-click matching
- Social sharing built-in
- Works in Warpcast

## 🎮 Demo

Try it live: `https://your-app.vercel.app`

Or search "Crypto Compatibility" in Warpcast!

## 🚀 Quick Deploy to Vercel

1. Click the "Deploy with Vercel" button above
2. Add environment variables:
   ```
   BASE_URL=https://your-app.vercel.app
   OPENAI_API_KEY=sk-your-key (optional)
   ```
3. Deploy!
4. Register on Farcaster: https://warpcast.com/~/developers

**That's it!** Your mini app is live in 5 minutes! 🎉

## 📚 Full Documentation

- [Vercel Deployment Guide](./VERCEL_DEPLOYMENT_GUIDE.md) - Step-by-step Vercel setup
- [Quick Start Guide](./QUICKSTART.md) - Local development
- [Project Overview](./PROJE_OZETI.md) - Turkish documentation

## 🏗️ Tech Stack

- **Backend**: FastAPI (Python 3.9+)
- **AI**: OpenAI GPT-4 (comedy generation)
- **Frames**: Farcaster Frames v2
- **Database**: PostgreSQL + Redis (optional)
- **Deployment**: Vercel
- **APIs**: Farcaster Social Graph, CoinGecko, OpenSea

## 📁 Project Structure

```
crypto-compatibility-engine/
├── app.py                          # Main FastAPI app
├── personality.py                  # Personality analyzer
├── comedy_generator.py             # AI comedy engine
├── database.py                     # Database layer (optional)
├── farcaster_client.py            # Farcaster API client
├── frame_generator/
│   └── frame_builder.py           # Frame generation
├── matching_algorithm/
│   └── matchmaker.py              # Matching logic
├── personality_profiles/
│   └── personalities.json         # 10+ personality types
├── comedy_templates/
│   └── comedy.json                # 100+ comedy templates
├── static/
│   └── images/                    # Frame images
└── vercel.json                    # Vercel configuration
```

## 🔧 Environment Variables

### Required
```bash
BASE_URL=https://your-app.vercel.app
```

### Optional
```bash
# AI Comedy (recommended)
OPENAI_API_KEY=sk-your-key

# Real Farcaster data
FARCASTER_API_KEY=your-key
FARCASTER_APP_FID=12345

# Database (works without it)
REDIS_HOST=your-redis.upstash.io
REDIS_PASSWORD=your-password
DATABASE_URL=postgresql://user:pass@host/db
```

## 🎯 Personality Types

1. **Bitcoin Purist** 🟠 - Only BTC, diamond hands
2. **DeFi Degenerate** 🌾 - Yield farming addict
3. **NFT Connoisseur** 🎨 - Art collector with taste
4. **Shitcoin Surfer** 🏄 - High risk, high reward
5. **Crypto Boomer** 👴 - ETH & BTC only
6. **Diamond Hands** 💎 - Never sells, HODL forever
7. **Paper Hands** 📄 - Takes profit, risk-averse
8. **Whale Watcher** 🐋 - Follows smart money
9. **DAO Builder** 🏗️ - Governance enthusiast
10. **Meme Lord** 😂 - Dogecoin & Shiba maximalist

## 🎨 Example Output

```
@vitalik & @elonmusk = 92% compatible! 🚀

Both of you:
• Dream of DAO on Mars
• Understand Dogecoin irony
• Complain about gas fees 😅

First date idea: Plan moon mission over Starlink! 🌕
```

## 🔥 Viral Features

- **Shareable results** with custom images
- **Celebrity matches** (hypothetical)
- **Funny commentary** on compatibility
- **Date suggestions** based on crypto interests
- **Social proof** with match counts

## 🛠️ Local Development

```bash
# Clone repo
git clone https://github.com/yourusername/crypto-compatibility-engine
cd crypto-compatibility-engine

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your keys

# Run locally
python app.py
# Visit http://localhost:8000
```

## 📊 API Endpoints

### Frames
- `GET /` - Initial frame
- `POST /api/analyze` - Analyze personality
- `POST /api/find-matches` - Find compatible users
- `POST /api/match/{index}` - Navigate matches

### API
- `GET /api/health` - Health check
- `GET /api/personalities` - List personality types
- `GET /api/user/{fid}` - Get user analysis
- `GET /api/compatibility/{fid1}/{fid2}` - Check compatibility

### Mini App
- `GET /.well-known/farcaster.json` - Mini app manifest
- `POST /api/webhook` - Mini app events

## 🐛 Troubleshooting

### Mini App Not Appearing in Search
1. Check manifest URL: `curl https://your-app.vercel.app/.well-known/farcaster.json`
2. Verify JSON format is correct
3. Re-register on Warpcast

### Buttons Not Working
- Frame meta tags are now Farcaster v2 compliant
- Clear Farcaster cache (wait 24 hours or contact support)
- Check Vercel logs for errors

### Database Errors
- App works without database (demo mode)
- Check `DATABASE_URL` format
- Use Upstash Redis (free tier) or disable database features

## 🎯 Roadmap

- [x] Basic personality analysis
- [x] Matching algorithm
- [x] AI comedy generation
- [x] Farcaster frames
- [x] Vercel deployment
- [ ] Real wallet analysis
- [ ] Historical transaction data
- [ ] Advanced NFT taste detection
- [ ] Leaderboard & streaks
- [ ] Premium features

## 💰 Monetization Ideas

1. **Premium Analysis** - Detailed compatibility reports
2. **Custom Frames** - Branded date frames
3. **Sponsored Matches** - "Ideal match" recommendations
4. **API Access** - Developers integrate matching
5. **NFT Badges** - Top compatible pairs get special badges

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repo
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open Pull Request

## 📄 License

MIT License - feel free to use for your own projects!

## 🙏 Acknowledgments

- Farcaster team for the amazing platform
- OpenAI for GPT-4 API
- Vercel for seamless deployment
- Crypto community for inspiration

## 📞 Contact

- Twitter: [@yourusername](https://twitter.com/yourusername)
- Warpcast: [@yourusername](https://warpcast.com/yourusername)
- Email: your@email.com

---

Made with 💜 for the Farcaster community

**Star ⭐ this repo if you found it helpful!**
