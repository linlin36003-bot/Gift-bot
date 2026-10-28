# Novel Gift Bot — GitHub + Railway

## 1. GitHub သို့တင်ရန်
1. ZIP ကို ဖြည်ပါ။
2. `bot.py`, `requirements.txt`, `Procfile`, `railway.json`, `README.md` ဖိုင်တွေကို GitHub repository အသစ်ထဲ upload လုပ်ပါ။

## 2. Railway မှာ Run ရန်
1. Railway ကိုဖွင့်ပြီး **New Project → Deploy from GitHub Repo** ကိုရွေးပါ။
2. ဒီ repository ကိုချိတ်ပါ။
3. Railway ရဲ့ **Variables** ထဲမှာ `BOT_TOKEN` ဆိုတဲ့ variable အသစ်ထည့်ပါ။
4. Value နေရာမှာ BotFather ကပေးတဲ့ Telegram bot token အသစ်ကိုထည့်ပါ။
5. Deploy လုပ်ပါ။ Logs ထဲမှာ `Bot running...` ပေါ်လာရင် စတင် run နေပါပြီ။

## လုံခြုံရေး
- Token ကို GitHub code ထဲ မထည့်ပါနှင့်။ Railway Variables ထဲမှာပဲ ထည့်ပါ။
- မူရင်းဖိုင်ထဲမှာ token တစ်ခု ပါနေခဲ့တဲ့အတွက် BotFather မှာ token ကို revoke လုပ်ပြီး token အသစ်ယူပါ။
- `BOT_ID` နဲ့ `BOT_USERNAME` нь bot reference information သာဖြစ်ပြီး `BOT_TOKEN` ကတော့ သင့်ကိုယ်ပိုင် bot token ဖြစ်ရပါမယ်။

## Bot အသုံးပြုနည်း
- Private chat မှာ `/start` သို့မဟုတ် `/help` ပို့ပါ။
- Character ID ပါတဲ့ message ကို bot ဆီပို့လျှင် `.cgift ID` ကို ပြပေးပါမယ်။
- Group ထဲမှာ bot ကို mention လုပ်နိုင်သလို card message ကို reply လုပ်ပြီး `/g` ပို့နိုင်ပါတယ်။
