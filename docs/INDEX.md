# Documentation Index

Welcome to AWS Zombie Hunter documentation!

## 📖 Getting Started

### For First-Time Users

1. **[README.md](../README.md)** — Quick overview and quick start (5 min read)
2. **[INSTALLATION.md](./INSTALLATION.md)** — Step-by-step setup guide (10 min)
3. **[USAGE.md](./USAGE.md)** — Try your first scan (5 min)

### For Experienced Users

1. **[CONFIGURATION.md](./CONFIGURATION.md)** — Advanced setup options (15 min)
2. **[ARCHITECTURE.md](./ARCHITECTURE.md)** — How it works internally (20 min)
3. **[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)** — Problem solving (on demand)

---

## 📚 Documentation Files

### README.md (Root)
**Purpose:** Quick overview, quick start, key features  
**Audience:** Everyone  
**Time:** 5 minutes  
**Read:** For high-level understanding and getting started

### INSTALLATION.md
**Purpose:** Detailed installation steps  
**Topics:**
- Prerequisites
- Step-by-step installation
- Virtual environment setup
- Credential configuration options
- Installation troubleshooting

**Read:** Before running for the first time

### CONFIGURATION.md
**Purpose:** Advanced configuration options  
**Topics:**
- AWS credentials setup (3 methods)
- IAM permissions
- Command-line options
- Output formats
- Performance tuning

**Read:** When customizing for your environment

### USAGE.md
**Purpose:** Practical usage examples  
**Topics:**
- Quick command examples
- Real-world scenarios
- Output interpretation
- Performance tips
- Integration examples (GitHub Actions, CloudWatch)

**Read:** Before and during first scans

### ARCHITECTURE.md
**Purpose:** Technical deep-dive  
**Topics:**
- System overview with diagrams
- Core components
- Data flow
- Performance characteristics
- Scalability analysis
- Thread safety
- Extension points

**Read:** When you need to understand internals or extend functionality

### TROUBLESHOOTING.md
**Purpose:** Problem resolution  
**Topics:**
- Credential issues
- Installation problems
- Runtime errors
- Output issues
- AWS API issues
- Permission issues
- Diagnostic commands
- Getting help

**Read:** When encountering issues

---

## 🎯 Quick Navigation by Task

### "I want to..."

#### Get started quickly
1. Read: [README.md](../README.md) (Quick Start section)
2. Run: `python main.py`
3. Check: [USAGE.md](./USAGE.md) for examples

#### Install properly
1. Follow: [INSTALLATION.md](./INSTALLATION.md)
2. Verify: `aws sts get-caller-identity`
3. Test: `python main.py --help`

#### Configure for my environment
1. Check: [CONFIGURATION.md](./CONFIGURATION.md)
2. Setup credentials using preferred method
3. Adjust: Worker count and region selection

#### Understand how it works
1. Read: [ARCHITECTURE.md](./ARCHITECTURE.md)
2. Explore: Code in `main.py`
3. Understand: Pagination and parallelism

#### Run scans for my use case
1. See: [USAGE.md](./USAGE.md) scenarios
2. Run: `python main.py [options]`
3. Analyze: Output CSV/JSON

#### Extend functionality
1. Study: [ARCHITECTURE.md](./ARCHITECTURE.md) extension points
2. Read: Code comments in `main.py`
3. Implement: Custom methods

#### Fix problems
1. Check: [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
2. Run: Diagnostic commands
3. Verify: Credentials and permissions

---

## 📊 Documentation Statistics

| File | Size | Topics | Read Time |
|------|------|--------|-----------|
| README.md | 5KB | Overview, Quick Start | 5 min |
| INSTALLATION.md | 2.3KB | Setup, Verify | 10 min |
| CONFIGURATION.md | 2.6KB | Credentials, Options | 15 min |
| USAGE.md | 4.4KB | Examples, Scenarios | 15 min |
| ARCHITECTURE.md | 7.9KB | Design, Performance | 20 min |
| TROUBLESHOOTING.md | 6.9KB | Issues, Solutions | On demand |
| **Total** | **30KB** | **30+ topics** | **~75 min** |

---

## 🔍 Search by Topic

### Credentials & Security
- [INSTALLATION.md](./INSTALLATION.md#step-4-configure-aws-credentials) — Credential setup
- [CONFIGURATION.md](./CONFIGURATION.md#aws-credentials-setup) — All credential methods
- [CONFIGURATION.md](./CONFIGURATION.md#iam-permissions) — Required permissions
- [TROUBLESHOOTING.md](./TROUBLESHOOTING.md#credential-issues) — Credential problems

### Installation & Setup
- [INSTALLATION.md](./INSTALLATION.md) — Full guide
- [INSTALLATION.md](./INSTALLATION.md#troubleshooting-installation) — Installation issues
- [CONFIGURATION.md](./CONFIGURATION.md) — Configuration options

### Usage & Examples
- [README.md](../README.md#-usage-examples) — Quick examples
- [USAGE.md](./USAGE.md) — Detailed examples
- [USAGE.md](./USAGE.md#real-world-scenarios) — Scenarios

### Command-Line Options
- [README.md](../README.md#-options) — Options summary
- [CONFIGURATION.md](./CONFIGURATION.md#command-line-options) — Detailed options

### Output & Reports
- [README.md](../README.md#-output) — Output formats
- [CONFIGURATION.md](./CONFIGURATION.md#output-files) — Output file details
- [USAGE.md](./USAGE.md#understanding-output) — Output interpretation

### Performance & Optimization
- [ARCHITECTURE.md](./ARCHITECTURE.md#performance-characteristics) — Performance analysis
- [CONFIGURATION.md](./CONFIGURATION.md#performance-tuning) — Tuning options
- [USAGE.md](./USAGE.md#performance-tips) — Practical tips

### Technical Details
- [ARCHITECTURE.md](./ARCHITECTURE.md) — Full architecture
- [ARCHITECTURE.md](./ARCHITECTURE.md#core-components) — Components
- [ARCHITECTURE.md](./ARCHITECTURE.md#data-flow) — Data flow

### Troubleshooting
- [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) — All issues
- [TROUBLESHOOTING.md](./TROUBLESHOOTING.md#credential-issues) — Credentials
- [TROUBLESHOOTING.md](./TROUBLESHOOTING.md#installation-issues) — Installation
- [TROUBLESHOOTING.md](./TROUBLESHOOTING.md#runtime-issues) — Runtime
- [TROUBLESHOOTING.md](./TROUBLESHOOTING.md#permission-issues) — Permissions

### Integration & Automation
- [USAGE.md](./USAGE.md#integration-examples) — GitHub Actions, CloudWatch

---

## 📝 Document Overview

### By Difficulty Level

**Beginner**
- README.md (Quick Start)
- INSTALLATION.md

**Intermediate**
- CONFIGURATION.md
- USAGE.md

**Advanced**
- ARCHITECTURE.md
- Code in main.py

---

## 🚀 Learning Path

### Path 1: Just Run It (10 minutes)
1. README.md → Quick Start
2. Run: `python main.py`
3. Done! View results

### Path 2: Proper Setup (30 minutes)
1. README.md → Overview
2. INSTALLATION.md → Full guide
3. CONFIGURATION.md → Setup options
4. USAGE.md → Try examples

### Path 3: Deep Understanding (90 minutes)
1. README.md → Full read
2. INSTALLATION.md → All steps
3. CONFIGURATION.md → All options
4. USAGE.md → All examples
5. ARCHITECTURE.md → Technical details
6. TROUBLESHOOTING.md → Reference

### Path 4: Problem Solving (On Demand)
1. TROUBLESHOOTING.md → Find your issue
2. Follow → Diagnostic steps
3. Check → Related docs

---

## 💡 Tips for Using Documentation

1. **Use Ctrl+F** to search within documents
2. **Follow links** to related topics
3. **Run examples** as you read
4. **Check Table of Contents** for quick navigation
5. **Read error messages** — documentation covers them

---

## 📞 Need More Help?

1. Check **[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)** for your issue
2. Run **diagnostic commands** (in Troubleshooting section)
3. Verify **AWS credentials**: `aws sts get-caller-identity`
4. Check **IAM permissions**: See [CONFIGURATION.md](./CONFIGURATION.md)

---

## 📦 Related Files

- `main.py` — Source code with comments
- `requirements.txt` — Dependencies
- `.env.example` — Example credentials file
- `LICENSE` — MIT license

---

**Last Updated:** Feb 25, 2026  
**Version:** AWS Zombie Hunter v2.1  
**Status:** Production Ready ✨
