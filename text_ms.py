hello_text = '''Hello!'''
def hello_text_reg(message, balance):
    return f'''Hello {message.first_name}!
You're balance a {balance} USDT'''


def balance(balance, link):
    return f'''***💰 Your balance***: {balance}
💳 Minimum withdrawal amount: ***500 USDT***

To pass verification and withdraw earned funds in the future, invite at least 3 people using your affiliate link.
👥 Your invite link: ***{link}***'''

def referal(referal_link):
    return f"***Invite a friend using your referral link***, and theyll receive 100 USDT credited to their account! Plus, as a thank you, youll earn 50 USDT for each friend you bring on board.\n\nYour referal link: ***{referal_link}***"

rules = '''Rules of Engagement

Account Creation: Each individual is allowed only one account. Multiple accounts for a single user are strictly prohibited and will result in immediate disqualification.

Referral Program: Share your unique referral link to invite friends. Your friends must use your link to sign up for you to receive the referral bonus. You get 50 USDT for every friend who joins, and your friend gets 100 USDT as a welcome bonus.

Earning Points: Points can be earned by participating in activities such as 'Earn' and 'Play'. The points system is subject to change at the discretion of the bot administrators.

Withdrawals: Points earned can be withdrawn as per the instructions under the 'Withdrawal' section. A minimum balance may be required to process a withdrawal.

Fair Play: Any attempt to use bots, duplicate accounts, or other unfair methods to gain points will be met with immediate account suspension.

Activity: Accounts must show regular activity as defined by the bot administrators. Inactive accounts may be subject to suspension or removal.

Updates: The bot administrators reserve the right to update these rules as necessary. It is the responsibility of the users to stay informed about any changes.

Support: For assistance, use the 'Help' or 'Support' options within the bot. Any abuse of the support system will not be tolerated.

Privacy: We respect your privacy. Your personal information will not be shared without your consent, except as required by law.

Compliance: By using this bot, you agree to abide by these rules and any additional terms presented to you during the use of the bot.'''


social = '''Select social network'''


work = "Technical work is underway"

def sub_tg(groupname):
    return f'Subscribe to the channel 💣 "{groupname}" and get 30 USDT on your balance!'

inactive = 'Sorry, task is inactive!'

fine_task = "✅You have been credited 30 USDT for a successfully completed task!"
not_fine_task = "❌ If you unsubscribe from the channel within 5 days, the bot will check and fine you 30 USDT"

bigmoney = '''📈Crypto Futures Signals
🚀ACCESS FROM 5,000$
👥Instagram Community
👉https://instagram.com/cryptofmoney'''

skip = "skipped!"