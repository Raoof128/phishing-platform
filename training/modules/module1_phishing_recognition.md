# Module 1: Recognizing Phishing Emails

## Learning Objectives

By the end of this module, you will be able to:
- Define phishing and understand its impact on organizations
- Identify common red flags in phishing emails
- Analyze email headers to verify sender authenticity
- Apply a systematic approach to evaluating suspicious emails

---

## What is Phishing?

**Phishing** is a type of cyber attack where malicious actors impersonate legitimate organizations or individuals to trick victims into:
- Revealing sensitive information (passwords, credit cards, personal data)
- Downloading malware or ransomware
- Transferring money or making unauthorized purchases
- Granting access to secure systems

### Why Phishing Works

Phishing exploits **human psychology** rather than technical vulnerabilities:
- **Urgency**: "Your account will be suspended in 24 hours!"
- **Authority**: "This is from the CEO/IT Department"
- **Fear**: "Unusual activity detected on your account"
- **Curiosity**: "You've won a prize!" or "See who viewed your profile"
- **Trust**: Mimicking familiar brands and services

---

## The Impact of Phishing

### Statistics
- **91%** of cyber attacks start with a phishing email
- **3.4 billion** phishing emails are sent daily worldwide
- **$4.9 million** average cost of a data breach
- **23%** of recipients open phishing emails
- **11%** click on malicious attachments

### Real-World Examples
- **2016 DNC Hack**: Phishing email led to major political data breach
- **Target Breach**: Started with phishing email to HVAC contractor
- **Australian ATO Scam**: Thousands fell victim to tax refund phishing

---

## Red Flags: How to Spot Phishing

### 1. Suspicious Sender Address

✅ **Legitimate**: `security@microsoft.com`  
❌ **Phishing**: `security@micr0s0ft.com` (zero instead of 'o')  
❌ **Phishing**: `support@microsoft-security.tk` (wrong domain)

**What to do**: Hover over the sender name to see the actual email address.

### 2. Generic Greetings

✅ **Legitimate**: "Dear John Smith" or "Hello John"  
❌ **Phishing**: "Dear Customer" or "Dear User"

**Why**: Legitimate companies usually personalize communications using your actual name.

### 3. Urgent or Threatening Language

❌ **Red Flag Phrases**:
- "Your account will be suspended immediately"
- "Urgent action required within 24 hours"
- "Verify your account now or lose access"
- "Unusual activity detected - click here NOW"

**Why**: Legitimate companies give reasonable timeframes and don't use extreme urgency.

### 4. Suspicious Links

**How to check**:
1. **Hover** over the link (don't click!)
2. Look at the URL in the bottom-left corner of your browser
3. Check if the domain matches the supposed sender

❌ **Phishing Link Examples**:
- `http://paypaI.com` (capital i instead of lowercase L)
- `https://login-microsoft.com` (extra hyphen)
- `http://secure-banking-verification.tk` (suspicious domain)

### 5. Unexpected Attachments

❌ **Dangerous File Types**:
- `.exe` - Executable files
- `.zip` - Compressed archives (may contain malware)
- `.scr` - Screensaver files (actually executables)
- `.js` - JavaScript files
- Office files with macros (`.docm`, `.xlsm`)

**Never open attachments from**:
- Unexpected emails
- Unknown senders
- Emails that don't match the supposed content

### 6. Poor Grammar and Spelling

❌ **Warning Signs**:
- Obvious spelling mistakes
- Poor grammar or awkward phrasing
- Inconsistent formatting
- Mix of fonts and styles

**Note**: Professional organizations proofread their communications.

### 7. Requests for Sensitive Information

🚨 **NEVER provide via email**:
- Passwords
- Social Security numbers
- Credit card numbers
- Bank account details
- Security question answers

**Important**: Legitimate companies NEVER ask for passwords or sensitive data via email.

### 8. Too Good to Be True

❌ **Common Scams**:
- "You've won a lottery you didn't enter"
- "Nigerian prince wants to share fortune"
- "Free iPhone - click here to claim"
- "You're selected for a $1000 gift card"

**Rule**: If it sounds too good to be true, it probably is.

---

## The SPAM Framework for Email Analysis

Use this systematic approach to evaluate suspicious emails:

### S - **Sender**
- Is the email address legitimate?
- Does it match the supposed organization?
- Hover to reveal actual address

### P - **Purpose**
- Why am I receiving this email?
- Did I expect this communication?
- Does the request make sense?

### A - **Attachments & Links**
- Are there unexpected attachments?
- Do links point to legitimate domains?
- Can I verify this through official channels?

### M - **Message Content**
- Is the tone urgent or threatening?
- Are there grammar/spelling errors?
- Does it request sensitive information?

---

## How to Verify Suspicious Emails

### 1. Check the Full Email Header
- In most email clients: View → Show Original / View Headers
- Look for "Return-Path" and "Received" fields
- Verify the originating server matches the organization

### 2. Contact the Sender Directly
- **Don't** use contact info from the suspicious email
- **Do** look up official contact information independently
- Call or email through official channels

### 3. Visit the Website Directly
- **Don't** click links in the email
- **Do** type the official website URL directly into your browser
- Check if the supposed issue exists in your account

### 4. Look for Digital Signatures
- Legitimate organizations often digitally sign emails
- Check for signature verification in your email client

---

## Real Phishing Examples (Study These)

### Example 1: Fake Password Reset

```
From: Microsoft Security <noreply@micr0soft-security.com>
Subject: Your password will expire today

Dear User,

Your Microsoft password is expiring in 2 hours. Click below 
to reset your password immediately or your account will be 
locked.

[Reset Password Now] ← suspicious link

Microsoft Security Team
```

**Red Flags**:
- ❌ Generic greeting ("Dear User")
- ❌ Misspelled domain (micr0soft)
- ❌ Extreme urgency (2 hours)
- ❌ Threatening tone (account locked)

### Example 2: Fake HR Document

```
From: HR Department <hr@company-internal.tk>
Subject: URGENT: New Policy Acknowledgment Required

Hi John,

Please review and sign the attached policy document 
within 24 hours. Failure to comply may result in 
disciplinary action.

[Download Document.exe] ← dangerous attachment

Thanks,
HR Team
```

**Red Flags**:
- ❌ Suspicious domain (.tk extension)
- ❌ Executable attachment (.exe)
- ❌ Threatening language
- ❌ Unusual urgency for policy document

---

## Practice Exercise

### Identify the Red Flags

**Email A**:
```
From: paypal@service-paypal.com
Subject: Account Limitation

Dear PayPal User,

We've noticed unusual activity on your account. Please 
verify your information within 12 hours to avoid permanent 
suspension.

Click here to verify: http://paypal-verify.tk
```

<details>
<summary>Click to see red flags</summary>

- ❌ Wrong domain (service-paypal.com, not paypal.com)
- ❌ Generic greeting
- ❌ Urgent timeframe (12 hours)
- ❌ Suspicious link domain (.tk)
- ❌ Threatening tone (permanent suspension)

</details>

---

## What to Do If You Receive a Phishing Email

### ✅ DO:
1. **Don't click** any links or open attachments
2. **Report it** to your IT security team immediately
3. **Delete** the email after reporting
4. **Warn** colleagues if it's a widespread attack
5. **Mark as spam** in your email client

### ❌ DON'T:
1. **Don't reply** to the email
2. **Don't forward** it to others (except IT security)
3. **Don't try** to "unsubscribe"
4. **Don't engage** with the sender

### Reporting Process
1. Forward the email to: **security@company.com**
2. Include the full email headers
3. Describe any actions you took (if any)
4. Wait for confirmation from IT security

---

## Quiz: Test Your Knowledge

1. **What percentage of cyber attacks start with phishing?**
   - A) 50%
   - B) 70%
   - C) 91%
   - D) 100%

2. **Which of these is a red flag in an email?**
   - A) Personalized greeting with your name
   - B) Urgent language threatening account suspension
   - C) Email from a known colleague
   - D) A PDF attachment you requested

3. **How should you verify a suspicious link?**
   - A) Click it to see where it goes
   - B) Hover over it to see the actual URL
   - C) Reply to the email asking if it's legitimate
   - D) Forward it to all your contacts

4. **What should you NEVER do via email?**
   - A) Send meeting invitations
   - B) Share your password
   - C) Respond to calendar requests
   - D) Attach documents

5. **What does the "S" in the SPAM framework stand for?**
   - A) Security
   - B) Sender
   - C) Spam
   - D) Subject

<details>
<summary>Click for answers</summary>

1. C) 91%
2. B) Urgent language threatening account suspension
3. B) Hover over it to see the actual URL
4. B) Share your password
5. B) Sender

</details>

---

## Key Takeaways

✅ **Remember**:
1. Phishing exploits human psychology, not just technology
2. Always verify sender authenticity before clicking or responding
3. Legitimate companies never ask for passwords via email
4. When in doubt, contact the organization through official channels
5. Report suspicious emails immediately to IT security

✅ **The Golden Rule**:
> **When in doubt, don't click it out!**

---

## Additional Resources

- **GoPhish Awareness**: https://getgophish.com/blog/
- **ACSC Phishing Guidance**: https://www.cyber.gov.au/
- **Google Phishing Quiz**: https://phishingquiz.withgoogle.com/
- **MailGuard Threat Intelligence**: https://www.mailguard.com.au/

---

**Next Module**: Module 2 - Social Engineering Tactics

**Estimated Time**: 15 minutes

---

*Security Awareness Training Program | © 2025*
