# RTL-SDR UDP Proxy - Future Enhancement

This directory contains design documents for a future enhancement to enable modern RTL-SDR library support while maintaining UDP control compatibility.

## Status: FUTURE IMPLEMENTATION

**Current Priority**: Get base codebase working with minimal changes  
**Future Priority**: Implement after MVP is stable

## Contents

- `DESIGN.md` - Complete technical design and architecture
- Future: Implementation files will go here

## Goal

Enable the cyberdeck to use modern RTL-SDR libraries (osmocom, rtl-sdr-blog) while maintaining the existing UDP control interface on port 6020.

## Benefits (When Implemented)

- Modern RTL-SDR hardware support (V4 dongles)
- Enhanced features (bias-tee, auto direct sampling)
- Performance improvements
- Backward compatibility with existing code

## Current Approach

For now, continue using the sysrun RTL-SDR fork as documented in the main project. This interoperability layer will be implemented once the base system is stable and working correctly.

## Implementation Timeline

1. **Phase 1**: Get current codebase working (CURRENT)
2. **Phase 2**: Stability and testing
3. **Phase 3**: Implement UDP proxy (FUTURE)
4. **Phase 4**: Backend abstraction and modern RTL-SDR support

---

*Filed away for future development - focusing on base functionality first.*