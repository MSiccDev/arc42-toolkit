# Contributing to arc42 Toolkit

Thank you for your interest in contributing!

We're excited to have you help make architecture documentation easier and more accessible for everyone. Whether you're fixing a typo, improving a skill, or sharing real-world examples, every contribution matters.

---

## 📋 Table of Contents

- [Welcome](#welcome)
- [How Can You Contribute?](#how-can-you-contribute)
- [Before You Start](#before-you-start)
- [Contribution Process](#contribution-process)
- [Quality Standards](#quality-standards)
- [Communication Channels](#communication-channels)
- [Developer Certificate of Origin (DCO)](#developer-certificate-of-origin-dco)
- [Code of Conduct](#code-of-conduct)
- [Recognition](#recognition)

---

## Welcome

This project aims to make arc42 architecture documentation accessible through AI coding assistants. We believe in:

- 📚 **Official Standards** - All content based on arc42.org sources
- 🤝 **Community Collaboration** - Everyone can contribute
- 🚀 **Practical Value** - Real-world usability matters
- ✅ **Quality First** - Maintain high standards
- 🌱 **Continuous Improvement** - We evolve as we learn

**Note:** These contribution guidelines are intentionally simple to start. We'll adjust and expand them based on community needs and project growth.

---

## How Can You Contribute?

### 🐛 Report Issues
Found a problem? Help us improve!
- Typos or grammar errors in a skill
- Inaccuracies compared to official arc42 standards
- Skills that don't work well with a particular AI tool
- Missing information or unclear explanations

**How:** [Open an issue](../../issues/new) with details

### 📝 Improve Skills
Make our content better!
- Fix typos and grammar in a skill
- Clarify confusing questions or checklist items
- Add helpful examples to skill output templates
- Sharpen skill effectiveness for specific AI tools
- Update outdated information

**How:** Submit a pull request

### 🌟 Share Examples
Real-world examples help everyone!
- Complete arc42 documentation for your project
- Domain-specific examples (microservices, embedded, etc.)
- Different project sizes (startup to enterprise)
- Success stories and lessons learned

**How:** Share in [Discussions](../../discussions) or submit as example

### 💡 Improve Skills
Make AI interactions better!
- Test skills with different AI tools (Claude Code, Copilot, Cursor, Codex)
- Improve question clarity and skill output templates
- Add edge case handling to quality checklists
- Share better patterns for interactive documentation

**How:** Submit a pull request with testing details

### 🔧 Tool Integration
Extend the ecosystem!
- IDE plugins or extensions
- CLI tools or scripts
- CI/CD integrations
- Template generators

**How:** Discuss in [Issues](../../issues) first, then submit PR

### 🌍 Translations
Make arc42 Toolkit global!
- Translate skills to other languages
- Localize examples
- Adapt for regional standards

**How:** Discuss in [Issues](../../issues) first

---

## Before You Start

### 1. Check Existing Work
- **Search [existing issues](../../issues)** - Someone might already be working on it
- **Check [pull requests](../../pulls)** - Avoid duplicate work
- **Read [Discussions](../../discussions)** - See ongoing conversations

### 2. Understand arc42
- Review [official arc42 documentation](https://docs.arc42.org)
- Understand the [arc42 philosophy](https://arc42.org)
- Familiarize yourself with the [Q42 quality model](https://quality.arc42.org)

### 3. Test Your Changes
- Validate against official arc42 standards
- Test skill changes with at least one AI tool (Claude Code, Copilot, or Cursor)
- Ensure markdown formatting is correct
- Check that examples are clear and accurate
- If you change anything under `skills/`, run `python scripts/sync-apm-skills.py` and then `python scripts/sync-apm-skills.py --check`

---

## Contribution Process

### For Small Changes (typos, small fixes)

1. **Fork** the repository
2. **Create a branch** (`git checkout -b fix-typo-section-5`)
3. **Make your changes**
4. **Sign your commit** with DCO (see below)
   ```bash
   git commit -s -m "Fix typo in Section 5 skill"
   ```
5. **Push** to your fork
6. **Open a Pull Request** with clear description

### For Larger Changes (new content, restructuring)

1. **Open an issue first** - Discuss your idea before investing time
2. **Wait for feedback** - We'll review within a week
3. **Get approval** - Ensure alignment with project goals
4. **Follow the same process** as small changes above

### What Happens Next?

- **Within 1 week:** We'll review your contribution
- **Feedback:** We may request changes or clarifications
- **Discussion:** Work with us to refine the contribution
- **Merge:** Once approved, we'll merge and celebrate! 🎉

---

## Quality Standards

All contributions should meet these standards:

### ✅ Content Requirements

- **Authentic:** Based on official arc42 sources (arc42.org, docs.arc42.org, quality.arc42.org)
- **Accurate:** No invented or speculative content
- **Clear:** Written for both humans and AI tools
- **Consistent:** Follows existing skill structure and formatting
- **Tested:** Validated with at least one AI tool

### ✅ Formatting Requirements

- **Markdown:** Properly formatted (use linters if needed)
- **Structure:** Follows existing file organization
- **Links:** All links work and point to correct resources
- **Examples:** Code examples use proper syntax highlighting

### ✅ Documentation Requirements

- **Rationale:** Explain WHY, not just WHAT
- **References:** Link to official arc42 sources
- **Examples:** Provide concrete, helpful examples
- **Completeness:** Don't leave obvious gaps

### ❌ What We Don't Accept

- Content not based on official arc42 standards
- Promotional material or spam
- Breaking changes without discussion
- Incomplete or untested contributions
- Disrespectful or unprofessional content

---

## Communication Channels

### GitHub Issues (Primary)
**Use for:**
- Bug reports
- Feature requests
- Documentation improvements
- Questions about contributing

[Open an issue](../../issues/new)

### GitHub Discussions (If project grows)
**Use for:**
- General questions
- Sharing experiences
- Community conversations
- Brainstorming ideas

[Start a discussion](../../discussions)

### Pull Request Comments
**Use for:**
- Specific feedback on contributions
- Technical discussions about changes
- Clarifications during review

---

## Developer Certificate of Origin (DCO)

We use the Developer Certificate of Origin (DCO) to ensure contributors have the right to submit their work. This is a simple, lightweight process.

### What is DCO?

By signing off your commits, you certify that:

```
(a) The contribution was created in whole or in part by me and I have 
    the right to submit it under the open source license indicated in 
    the file; or

(b) The contribution is based upon previous work that, to the best of 
    my knowledge, is covered under an appropriate open source license 
    and I have the right under that license to submit that work with 
    modifications, whether created in whole or in part by me, under 
    the same open source license (unless I am permitted to submit under 
    a different license), as indicated in the file; or

(c) The contribution was provided directly to me by some other person 
    who certified (a), (b) or (c) and I have not modified it.

(d) I understand and agree that this project and the contribution are 
    public and that a record of the contribution (including all personal 
    information I submit with it, including my sign-off) is maintained 
    indefinitely and may be redistributed consistent with this project 
    or the open source license(s) involved.
```

### How to Sign Off

Simply add the `-s` flag when committing:

```bash
git commit -s -m "Your commit message"
```

This automatically adds a `Signed-off-by` line:

```
Signed-off-by: Your Name <your.email@example.com>
```

**Important:** Use your real name (no pseudonyms or anonymous contributions, please).

### Forgot to Sign?

If you forget to sign a commit, you can amend it:

```bash
git commit --amend --signoff
```

For multiple commits, you may need to rebase and sign each:

```bash
git rebase --signoff HEAD~3  # for last 3 commits
```

---

## Code of Conduct

### Our Standards

We are committed to providing a welcoming and inclusive environment. We expect all contributors to:

- **Be Respectful** - Treat everyone with respect and consideration
- **Be Constructive** - Provide helpful feedback and criticism
- **Be Professional** - Maintain professional conduct in all interactions
- **Be Inclusive** - Welcome people of all backgrounds and experience levels
- **Be Patient** - Remember that people have different skill levels and perspectives

### Unacceptable Behavior

- Harassment, discrimination, or hate speech
- Personal attacks or insults
- Trolling or deliberately disruptive behavior
- Spam or promotional content
- Sharing private information without consent

### Enforcement

Violations of the code of conduct may result in:
1. Warning
2. Temporary ban from project
3. Permanent ban from project

Report violations to the project maintainer.

---

## Recognition

We value and recognize all contributions!

### How We Credit Contributors

- **CONTRIBUTORS.md** - All contributors listed in dedicated file
- **GitHub Contributors** - Automatically tracked by GitHub
- **README.md** - Link to CONTRIBUTORS.md in main README
- **Release Notes** - Significant contributions mentioned in releases

### Types of Contributions We Recognize

- Code contributions (PRs merged)
- Documentation improvements
- Bug reports and issue triage
- Example submissions
- Community support in discussions
- Testing and validation
- Ideas and suggestions that shape the project

**Everyone who helps make this project better deserves recognition!** 🌟

---

## Questions?

- **General questions:** [Open an issue](../../issues/new)
- **Contribution questions:** Check existing issues or open a new one
- **Need help getting started?** We're here to help - just ask!

---

## Thank You! 🙏

Every contribution, no matter how small, helps make architecture documentation more accessible. We appreciate your time and effort in making this project better.

**Ready to contribute?** Pick an issue, fork the repo, and let's build something great together!

---

**Project maintained with ❤️ by the community**

*These guidelines will evolve as the project grows. Feedback welcome!*
