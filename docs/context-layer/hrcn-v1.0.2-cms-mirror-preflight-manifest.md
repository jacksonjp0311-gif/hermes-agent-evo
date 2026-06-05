# HRCN v1.0.2 CMS Mirror Preflight Manifest

- passed: true
- source: `C:\Users\jacks\OneDrive\Desktop\cybernetic-memory-system`
- target: `cms/`
- source git commit: `d650f4f3dd397ebe49e3fb7a38959bda1af72415`
- source git branch: `main`
- source remote: `https://github.com/jacksonjp0311-gif/cybernetic-memory-system.git`
- file count: 712
- total bytes: 3594235
- secret scan passed: true
- authorization phrase received: True

## Rollback / Removal

```powershell
Remove-Item -Recurse -Force .\cms
```

## Boundary

This preflight authorizes a read-only mirror snapshot only. It does not create runtime integration or CMS authority.
