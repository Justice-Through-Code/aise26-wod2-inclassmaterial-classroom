### Phase 1
C Rotate/revoke the compromised credentials immediately

Since credentials are publicly exposed, we need to assume they are compromised. Cleaning up the git history cannot change the possibility that someone captured those credentials and are trying to use them.

### Phase 2

I would choose revert if its a large project, since someone else might have pulled the repo. Otherwise, if we can coordinate all of the team members, I would choose rewrite.

### Phase 3

I would write a summary, including timestamps, of the incident, and identify the root cause of the event. I would then write suggested security practices to prevent something like this from happening again.


# Discussion Questions
- I would use revert over rewrite on public repos. Either way, I would rewrite the git history once everyone can coordinate.
- I would notify my manager and tech lead for this incident. If there's a security team, I would let them know as well.
- I would use github secret scanning to automatically detect secrets. I would apply the least privilege principle, making sure the API keys used have only enough privilege to access necessary resources. I would also rotate keys regularly.