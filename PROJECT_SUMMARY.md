# Phishing Attack Simulation and Training Platform - Project Summary

## Overview

A comprehensive phishing simulation and security awareness training platform built with **GoPhish** and **Python automation**. This platform enables organizations to conduct realistic phishing simulations, track user responses, assess risk levels, and provide targeted security training.

## 🎯 Project Goals

- **Defensive Security**: Train employees to recognize and resist phishing attacks
- **Risk Assessment**: Identify high-risk users through behavioral analysis
- **Automated Training**: Assign personalized training based on performance
- **Comprehensive Analytics**: Track metrics and measure improvement over time
- **Enterprise-Ready**: Scalable architecture suitable for organizations of all sizes

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Phishing Platform                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐      ┌──────────────┐     ┌────────────┐  │
│  │   GoPhish   │◄────►│   Python     │◄───►│  Analytics │  │
│  │  (Core)     │      │  Automation  │     │  Dashboard │  │
│  └─────────────┘      └──────────────┘     └────────────┘  │
│         │                     │                    │         │
│         ▼                     ▼                    ▼         │
│  ┌─────────────┐      ┌──────────────┐     ┌────────────┐  │
│  │   Email     │      │   Training   │     │   Reports  │  │
│  │  Templates  │      │  Assignment  │     │   & Risk   │  │
│  └─────────────┘      └──────────────┘     └────────────┘  │
│         │                     │                    │         │
│         ▼                     ▼                    ▼         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Target Users (Employees)                │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 📂 Project Structure

```
phishing-platform/
├── automation/              # Python automation scripts
│   ├── campaign_manager.py  # Campaign creation & management
│   ├── analytics.py         # Analytics & risk scoring
│   ├── training_automation.py # Training assignment
│   ├── user_import.py       # User/group import
│   └── config/              # Configuration files
│
├── templates/               # Email & landing page templates
│   ├── emails/              # 5 phishing email templates
│   │   ├── password_reset.html
│   │   ├── hr_document.html
│   │   ├── security_alert.html
│   │   ├── ceo_fraud.html
│   │   └── account_verification.html
│   └── landing_pages/       # 5 landing pages
│       ├── office365_login.html
│       ├── gmail_login.html
│       ├── corporate_portal.html
│       ├── awareness_page.html
│       └── training_redirect.html
│
├── gophish/                 # GoPhish installation
├── docs/                    # Documentation
├── training/                # Training modules
└── dashboard/               # Analytics dashboard (Flask)
```

## ✨ Key Features

### 1. **Realistic Phishing Templates**
- ✅ Password reset notifications
- ✅ HR document requests
- ✅ Security alerts
- ✅ CEO fraud / urgency attacks
- ✅ Account verification requests

### 2. **Professional Landing Pages**
- ✅ Office 365 login page
- ✅ Gmail login page
- ✅ Corporate portal
- ✅ Awareness/training redirect pages
- ✅ Mobile-responsive design

### 3. **Python Automation**
- ✅ Campaign creation & scheduling
- ✅ User import from CSV
- ✅ Risk score calculation
- ✅ Automated report generation
- ✅ Training assignment based on risk

### 4. **Analytics & Reporting**
- ✅ Campaign performance metrics
- ✅ User risk scoring (0-100)
- ✅ Individual user tracking
- ✅ Department/group comparisons
- ✅ HTML/CSV report generation

### 5. **Training Integration**
- ✅ Automated training assignment
- ✅ Risk-based module selection
- ✅ Progress tracking
- ✅ Email notifications

## 📊 Key Metrics Tracked

| Metric | Description | Calculation |
|--------|-------------|-------------|
| **Open Rate** | % of emails opened | (Opened / Sent) × 100 |
| **Click Rate** | % of users who clicked link | (Clicked / Sent) × 100 |
| **Submission Rate** | % who entered credentials | (Submitted / Sent) × 100 |
| **Report Rate** | % who reported email | (Reported / Sent) × 100 |
| **Risk Score** | User vulnerability score (0-100) | Weighted algorithm based on history |

## 🎓 Training Modules Included

1. **Phishing Recognition** - Identifying red flags and suspicious indicators
2. **Social Engineering** - Understanding manipulation tactics
3. **Email Safety** - Best practices for secure email handling
4. **Incident Response** - What to do when phished

## 🔧 Technologies Used

| Component | Technology |
|-----------|------------|
| **Phishing Engine** | GoPhish v0.12.1 |
| **Backend** | Python 3.10+ |
| **Web Framework** | Flask 3.0 |
| **Database** | SQLite / PostgreSQL |
| **Analytics** | Pandas, Matplotlib, Plotly |
| **Email** | SMTP (Gmail/SendGrid) |
| **Frontend** | HTML5, CSS3, Bootstrap 5 |

## 🚀 Quick Start

```bash
# 1. Install GoPhish
cd gophish && ./gophish

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Configure API key
nano automation/config/api_config.yaml

# 4. Test connection
python3 automation/campaign_manager.py --test

# 5. Import users
python3 automation/user_import.py --csv users.csv --group "Test Group"

# 6. Create campaign
python3 automation/campaign_manager.py \
  --create \
  --name "Test Campaign" \
  --template "Password Reset" \
  --landing-page "Office 365 Login" \
  --smtp "Gmail SMTP" \
  --group "Test Group"
```

## 📈 Success Metrics & Goals

### Target KPIs
- ✅ Reduce click rate by **50%** over 3 campaigns
- ✅ Increase report rate to **>20%**
- ✅ Achieve **90%+** training completion
- ✅ Identify and remediate high-risk users (3+ failures)

### Risk Level Distribution
- **High Risk (70-100)**: Advanced training + monitoring
- **Medium Risk (40-69)**: Standard training modules
- **Low Risk (0-39)**: Basic awareness training

## 🔐 Security & Ethics

### ✅ Best Practices
- Get **written authorization** before campaigns
- Clearly define **scope and boundaries**
- **Secure storage** of captured data
- Provide **immediate feedback** after simulation
- Focus on **education, not punishment**

### ⚠️ Important Considerations
- Never target personal email addresses
- Use clearly fake domains
- Inform participants after completion
- Comply with local laws and regulations
- Never shame individuals publicly

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| `README.md` | Project overview and features |
| `GETTING_STARTED.md` | Quick start guide (30 minutes) |
| `docs/installation_guide.md` | Detailed installation instructions |
| `docs/user_manual.md` | Platform usage guide |
| `docs/api_documentation.md` | Python API reference |
| `TROUBLESHOOTING.md` | Common issues and solutions |

## 🎯 Use Cases

### 1. **Quarterly Security Testing**
Run progressive campaigns to test employee awareness and measure improvement.

### 2. **New Hire Onboarding**
Assess baseline security awareness of new employees.

### 3. **Department Risk Assessment**
Compare phishing susceptibility across different departments.

### 4. **Compliance Training**
Meet regulatory requirements for security awareness training.

### 5. **Incident Response Practice**
Train users to recognize and report suspicious emails.

## 💼 Portfolio Value

### For Australian Employers
✅ **Industry-Relevant**: Phishing is #1 attack vector in Australian organizations  
✅ **Practical Skills**: Demonstrates hands-on security awareness expertise  
✅ **Enterprise Tools**: Experience with professional pentesting framework (GoPhish)  
✅ **Automation**: Python scripting for security operations  
✅ **Analytics**: Data-driven security metrics and reporting  
✅ **Scalability**: Architecture suitable for SME to enterprise scale  

### Demonstrates Competencies In
- Social engineering and human attack vectors
- Security awareness training program management
- Python automation and API integration
- Risk assessment and behavioral analysis
- Security metrics and reporting
- SMTP and email infrastructure
- Web development (HTML/CSS/JavaScript)
- Database management (SQLite/PostgreSQL)

## 🔄 Continuous Improvement Cycle

```
1. PLAN              2. EXECUTE         3. MEASURE         4. IMPROVE
   │                    │                  │                  │
   ├─ Define scope     ├─ Send phishing  ├─ Track metrics  ├─ Assign training
   ├─ Select targets   ├─ Monitor clicks ├─ Calculate risk ├─ Adjust difficulty
   ├─ Choose template  ├─ Capture data   ├─ Generate report├─ Update templates
   └─ Schedule launch  └─ Track timeline └─ Identify trends└─ Iterate campaign
                                              │
                                              └──────────────► REPEAT
```

## 🌟 Key Achievements

- ✅ **5 realistic phishing email templates** covering major attack vectors
- ✅ **5 professional landing pages** with credential capture
- ✅ **4 Python automation modules** (1000+ lines of code)
- ✅ **Risk scoring algorithm** with behavioral analysis
- ✅ **Automated training assignment** based on performance
- ✅ **Comprehensive reporting** with HTML/CSV export
- ✅ **Complete documentation** (installation, usage, API reference)
- ✅ **Production-ready architecture** for real-world deployment

## 📊 Expected Results

### After 3 Months
- **Baseline established**: Initial metrics captured
- **Training delivered**: All users complete baseline training
- **Trends identified**: High-risk users identified
- **Awareness increased**: Report rate improves

### After 6 Months
- **Click rate reduced**: 30-50% reduction in phishing susceptibility
- **Report rate increased**: 15-20% of users reporting suspicious emails
- **Risk scores improved**: Repeat offenders reduced by 60%
- **Culture shift**: Security awareness embedded in organization

## 🛠️ Future Enhancements

- [ ] Two-factor authentication bypass simulation
- [ ] SMS/text message phishing (smishing)
- [ ] Voice phishing (vishing) scenarios
- [ ] QR code phishing attacks
- [ ] Dark mode for dashboard
- [ ] Multi-language support
- [ ] Integration with SIEM platforms
- [ ] Machine learning for adaptive difficulty

## 📞 Support & Resources

- **Installation Issues**: See `docs/installation_guide.md`
- **Usage Questions**: See `docs/user_manual.md`
- **Troubleshooting**: See `TROUBLESHOOTING.md`
- **GoPhish Docs**: https://docs.getgophish.com/

## 📄 License & Legal

This platform uses GoPhish (MIT License) and includes custom automation scripts. 

**⚠️ Legal Disclaimer**: This platform is designed for authorized security awareness training and defensive security purposes only. Unauthorized use may be illegal in your jurisdiction. Users are responsible for obtaining proper authorization and complying with all applicable laws.

---

## 🏆 Conclusion

This **Phishing Attack Simulation and Training Platform** demonstrates comprehensive understanding of:
- Social engineering attack vectors
- Security awareness training methodologies  
- Python automation and API integration
- Risk assessment and behavioral analytics
- Professional security tooling and workflows

**Perfect for**: Security Analyst, SOC Analyst, Security Consultant, or GRC Analyst roles in Australian organizations.

---

**Built with security, education, and ethics in mind** 🔒🎓

*Last Updated: October 2025*
