# RTL-SDR UDP Control Interoperability Layer Design

**Status**: Future Enhancement - Filed for Later Implementation  
**Priority**: Post-MVP (after getting base codebase working)  
**Goal**: Enable modern RTL-SDR libraries while maintaining UDP control compatibility

## Problem Statement

The cyberdeck project currently uses the sysrun RTL-SDR fork specifically for its UDP control capability (port 6020). Newer RTL-SDR libraries (osmocom, rtl-sdr-blog) offer better features and hardware support but lack UDP control.

## Proposed Solution: Interoperability Layer

Create a proxy server that maintains UDP control compatibility while enabling use of modern RTL-SDR backends.

## Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Cyberdeck     │    │   UDP Control    │    │   RTL-SDR       │
│   API Client    │◄──►│   Proxy Server   │◄──►│   Backend       │
│                 │    │                  │    │   (Any Version) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
     UDP 6020                   |                       |
                                ▼                       ▼
                     ┌──────────────────┐    ┌─────────────────┐
                     │ Command Abstraction │  │ RTL-SDR Backends │
                     │     Layer          │  │ • osmocom       │
                     └──────────────────┘    │ • rtl-sdr-blog  │
                                             │ • sysrun        │
                                             │ • pyrtlsdr      │
                                             └─────────────────┘
```

## Key Components

### 1. UDP Control Proxy
- Maintains compatibility with port 6020
- Parses sysrun UDP protocol commands
- Translates to appropriate backend commands
- Manages process lifecycle

### 2. RTL-SDR Abstraction Layer
- Plugin system for different RTL-SDR libraries
- Unified command interface across backends
- Auto-detection of available installations
- Feature capability detection

### 3. Process Manager
- Handles rtl_tcp/rtl_fm lifecycle management
- Automatic restart on parameter changes
- Health monitoring and recovery
- Resource cleanup

### 4. Configuration System
- Backend selection and preferences
- Feature enablement flags
- Performance tuning parameters
- Fallback mechanisms

## Benefits

✅ **Backward Compatibility** - Existing cyberdeck code unchanged  
✅ **Modern RTL-SDR Support** - Use latest drivers (RTL-SDR Blog V4, etc.)  
✅ **Flexible Backends** - Switch between rtl-sdr versions without code changes  
✅ **Enhanced Features** - Access bias-tee, auto-direct sampling, etc.  
✅ **Performance** - Leverage latest RTL-SDR optimizations  

## Implementation Phases

### Phase 1: Core Infrastructure
- Create `src/rtl_interop/` directory structure
- Implement UDP proxy server (port 6020)
- Add basic backend abstraction
- Create process manager for rtl_tcp/rtl_fm

### Phase 2: Backend Support
- Implement sysrun backend (existing behavior)
- Add osmocom backend support
- Add rtl-sdr-blog backend support
- Add pyrtlsdr Python library backend

### Phase 3: Enhanced Features
- Configuration-driven backend selection
- Additional UDP commands for new features
- Performance monitoring and health checks
- Automatic backend detection

### Phase 4: Integration & Testing
- Cyberdeck API integration
- Comprehensive testing with different hardware
- Migration documentation
- Performance benchmarking

## File Structure

```
src/rtl_interop/
├── __init__.py
├── udp_proxy.py           # Main UDP server (port 6020)
├── backends/
│   ├── __init__.py
│   ├── base.py           # Abstract backend interface
│   ├── sysrun.py         # Original sysrun backend
│   ├── osmocom.py        # Official osmocom backend
│   ├── rtlsdr_blog.py    # RTL-SDR Blog backend
│   └── pyrtlsdr.py       # Python library backend
├── config.py             # Backend configuration
├── process_manager.py    # RTL process lifecycle
└── commands.py          # UDP command parser
```

## UDP Command Translation Examples

```python
# Sysrun UDP Commands → Modern RTL-SDR
"freq 144800000"     → rtl_tcp restart with new frequency
"mode fm"           → rtl_fm restart with FM demodulation  
"gain 48"           → Update gain parameter
"bias on"           → Enable bias-tee (if supported)
"direct_sampling on" → Enable direct sampling mode
```

## Backend Support Matrix

| Feature              | sysrun | osmocom | rtl-sdr-blog |
|---------------------|--------|---------|--------------|
| UDP Control         |   ✓    |  Proxy  |    Proxy     |
| Bias Tee           |   ✗    |  Basic  |   Enhanced   |
| Auto Direct Sampling|   ✗    |   ✗     |      ✓       |
| V4 Hardware        |   ✗    |   ✓     |      ✓       |
| Performance        |  Good  | Better  |     Best     |

## Configuration Example

```ini
[rtl_interop]
# Backend selection: sysrun, osmocom, rtlsdr_blog, pyrtlsdr
backend = rtlsdr_blog
udp_port = 6020
auto_restart = yes
enable_enhanced_features = yes

[rtlsdr_blog]
binary_path = /usr/local/bin/rtl_tcp
enable_auto_direct_sampling = yes
enable_bias_tee = yes
default_gain = 48

[osmocom]
binary_path = /usr/bin/rtl_tcp
enable_experimental_features = no
```

## Migration Strategy

1. **Zero-Downtime**: Proxy runs alongside existing sysrun
2. **Gradual Rollout**: Test with specific radios first  
3. **Fallback**: Auto-fallback to sysrun if newer backend fails
4. **Validation**: Comprehensive testing with all cyberdeck features

## Testing Plan

### Unit Tests
- UDP command parsing
- Backend interface compliance
- Process lifecycle management
- Configuration validation

### Integration Tests
- Full cyberdeck API compatibility
- Multi-backend switching
- Hardware compatibility tests
- Performance benchmarks

### Hardware Tests
- RTL-SDR Blog V3/V4 dongles
- Generic RTL-SDR dongles
- Multiple simultaneous dongles
- Bias-tee functionality

## Risk Mitigation

### Compatibility Risks
- Maintain exact UDP protocol compatibility
- Comprehensive regression testing
- Automatic fallback mechanisms

### Performance Risks
- Benchmark against current sysrun performance
- Optimize proxy overhead
- Asynchronous command processing

### Deployment Risks
- Phased rollout strategy
- Easy rollback mechanism
- Extensive documentation

## Success Criteria

1. **100% UDP Protocol Compatibility** - All existing cyberdeck commands work unchanged
2. **Enhanced Hardware Support** - RTL-SDR Blog V4 and newer dongles supported
3. **Performance Parity** - No performance degradation vs. current sysrun
4. **Feature Access** - Bias-tee and auto-direct sampling available
5. **Easy Migration** - Simple configuration change to switch backends

## Future Considerations

- WebSocket control interface for modern web UIs
- gRPC API for high-performance control
- Multi-SDR coordination and management
- Remote SDR support over network
- Integration with GNU Radio workflows

---

**Note**: This design is filed for future implementation after the base cyberdeck codebase is stable and working as intended. Focus remains on minimal changes to achieve working state first.