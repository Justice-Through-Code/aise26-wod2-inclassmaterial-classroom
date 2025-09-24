# Git Crisis Management Exercise - Theory Breakout

**Duration:** 15 minutes  
**Format:** Group discussion (no commands run)  
**Objective:** Think through how to respond to Git disasters under time pressure

---

## 🚨 EMERGENCY SCENARIO

**ALERT:** You've just discovered that API keys were accidentally committed to your main branch **3 commits ago**. The repository is **PUBLIC** and the keys are **currently active** in your production system.

**Timeline:** This happened 2 hours ago. You need to respond immediately.

---

## Your Emergency Response (10 minutes, discussion)

### Phase 1: Immediate Damage Control (First 3 minutes)

**CRITICAL: What's your first action and why?**

Choose the correct first step:
- [ ] A) Remove the secrets from the current code
- [ ] B) Make the repository private
- [x] C) Rotate/revoke the compromised credentials immediately
- [ ] D) Delete the problematic commits

**Why is this the right first step?**
- Why: Even if you delete the keys from Git, they’re already out there — anyone could’ve copied them in the last 2 hours. So the very first thing is to disable those old keys and create new ones.

### Phase 2: Git History Cleanup (Next 4 minutes)

**Situation Assessment:**
```bash
git log --oneline -5
a1b2c3d Fix user authentication bug
e4f5g6h Update README documentation  
i7j8k9l Add production configuration  ← API keys are in this commit! <--BAD COMMIT(KEYS INSIDE)
m1n2o3p Add user management features
q4r5s6t Initial project setup
```

**Discuss your Git recovery approach:**

**Option A: Safe Revert (if others might have pulled)**
```bash
git revert i7j8k9l
# Creates new commit that removes the secrets
```

**Option B: History Rewrite (if you're sure no one else pulled)**
```bash
git rebase -i HEAD~3
# Remove the problematic commit entirely
```

**Which option would you choose and why?**
👉 For most class/team projects, the safe answer is: use git revert. That way, you don’t rewrite history and confuse everyone. It just makes a new commit that “undoes” the secrets.

### Phase 3: Prevention Implementation (Last 3 minutes)

**Set up prevention measures:**

1. **Update .gitignore:**
```bash
# Add to .gitignore
.env
config/secrets/
*.key
credentials.json
```

2. **Create pre-commit hook (example):**
```bash
#!/bin/bash
# Check for secrets before commit
if grep -r "api_key\s*=" . ; then
    echo "❌ API key found! Use environment variables."
    exit 1
fi
```

3. **Document the incident:**
What would you write in your incident report?
chatgpt:
## Incident Report – Exposed Credentials

**What happened (Summary):**
API keys were accidentally committed to main in commit `i7j8k9l` and pushed to a public repo.

**Timeline:**
- T0: Commit with keys pushed to GitHub (public)
- T+2h: Exposure discovered
- T+2h + 5m: Keys rotated/revoked
- T+2h + 15m: Git history cleaned (revert)
- T+2h + 30m: Prevention measures added (.gitignore, pre-commit hook, docs)

**Impact:**
Potential unauthorized access with exposed keys while active. No confirmed misuse yet.

**Immediate Actions Taken:**
- Rotated/revoked exposed credentials immediately.
- Removed secrets from code and created a clean commit (revert).
- Searched history for other secrets.
- Opened ticket to monitor logs for suspicious activity.

**Root Cause:**
Secrets were stored in code instead of environment variables. No pre-commit scanning in place.

**Prevention / Follow-ups:**
- Use environment variables and a `.env` file (ignored by git).
- Add pre-commit secret scanning.
- Team reminder/training on secret handling.
- Consider enabling repo secret scanning in CI.

---

## Team Discussion (5 minutes)

**Share with your breakout room:**

### Crisis Response Questions:
1. **Speed vs. Safety:** When would you choose history rewrite vs. revert?
Revert if anyone else might have pulled the bad commit (safer, no history rewrite).
Rewrite (rebase -i) only if it’s certain nobody else has it yet (solo work).

2. **Communication:** Who would you notify during this incident?
Teammates/instructor, whoever manages the credentials (DevOps/security), and anyone relying on the keys (downstream services).

3. **Prevention:** What other security measures could prevent this?
Environment variables + .env (gitignored).
Secret scanning (pre-commit, CI, or GitHub’s built-ins).
Least-privilege keys and key rotation policy.
Code reviews with a “no secrets in code” checklist.




### Git Command Practice:
1. **Have you used `git revert` vs `git rebase -i` before?**
NOPE
2. **What's the difference between `git reset` and `git revert`?**
revert makes a new commit that undoes another (safe on shared branches).
rebase -i edits history (only safe if nobody else has pulled).
reset moves your branch pointer (can drop commits from history).
revert adds a new commit to undo changes (history stays intact).

3. **When is `git push --force` acceptable?**
On your own branch or when the team explicitly agrees.
Prefer --force-with-lease to avoid overwriting others’ work.



### Real-World Experience:
1. **Has anyone experienced a similar incident?**
2. **What security practices does your workplace use?**
3. **How would your team handle credential rotation?**

---

---

## Common Mistakes to Avoid

❌ **Wrong:** Trying to fix Git history before rotating credentials  
✅ **Right:** Rotate credentials first, then clean history

❌ **Wrong:** Using `git push --force` without checking with team  
✅ **Right:** Use `git push --force-with-lease` or coordinate with team

❌ **Wrong:** Only removing secrets from current code  
✅ **Right:** Remove from Git history too (if possible)

❌ **Wrong:** Not implementing prevention measures  
✅ **Right:** Set up hooks and scanning to prevent recurrence

---

## Git Recovery Commands Reference

```bash
# Find lost commits
git reflog

# See what changed in a commit
git show <commit-hash>

# Undo last commit, keep changes
git reset --soft HEAD~1

# Undo last commit, lose changes  
git reset --hard HEAD~1

# Undo specific commit safely
git revert <commit-hash>

# Interactive rebase to edit history
git rebase -i HEAD~N

# Check if it's safe to force push
git push --force-with-lease
```

---

## Real-World Context

**This scenario is extremely common:**
- GitHub's secret scanning finds **millions** of exposed credentials
- **Average detection time:** 20 days for exposed secrets
- **Real impact:** AWS bills of $50,000+ from compromised keys
- **Legal implications:** GDPR fines, compliance violations

**Your response time matters:**
- **Under 1 hour:** Minimal impact if caught early
- **1-24 hours:** Moderate risk, require monitoring
- **Over 24 hours:** High risk, assume compromise

The skills you practice here directly protect production systems and prevent security incidents that can cost companies millions of dollars.