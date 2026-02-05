# Neural Arena Debug Mode

Debug the following issue: $ARGUMENTS

---

## Debug Framework for Neural Arena

### Step 1: Observe
- [ ] Check screenshots at `/Users/reemifai/hub/neural-arena/screenshots/gameplay_capture/`
- [ ] Read `capture_info.txt` for context
- [ ] Note: Is this 2D mode, 3D mode, or both?
- [ ] What IS happening vs what SHOULD happen?

### Step 2: Hypothesize
List ALL possible causes (don't assume the obvious):
- Effect not in SIGNATURE_EFFECTS?
- Effect has no renderer?
- Effect not being pushed to fxQueue?
- Conditional push preventing execution?
- Duration too short?
- Position/coordinates wrong?
- startTime/lifecycle issue?
- Mode-specific bug (2D vs 3D)?

### Step 3: Trace Data Flow
Follow the effect lifecycle:
```
1. CREATION: Where is fxQueue.push() called? (App.tsx)
2. TRANSFER: How does it reach the renderer? (React state)
3. PROCESSING: Is it being processed? (Effects3D.tsx useEffect)
4. RENDERING: Is the renderer executing? (Effects3D.tsx if block)
5. CLEANUP: Is it being removed too early? (useFrame cleanup)
```

### Step 4: Verify
- Search for the effect type in Effects3D.tsx
- Search for fxQueue.push with the effect type in App.tsx
- Check SIGNATURE_EFFECTS array
- Check duration calculation

### Step 5: Fix
- Apply minimal change to fix root cause
- Test in BOTH 2D and 3D modes
- Run `npm run build` to verify

### Step 6: Validate
- Visual inspection confirms expected behavior
- No new errors introduced
- Build succeeds

---

**Now debug the issue above using this framework.**
