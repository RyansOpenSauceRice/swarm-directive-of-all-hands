# Development Philosophy

## Open Source Preference
- Prefer existing open source solutions over custom implementations
- Choose well-maintained libraries with active communities
- Favor MIT/Apache licensed projects when possible
- Document all third-party dependencies

## Library Selection Criteria
1. Maturity (release history, contributors)
2. Documentation quality
3. Community support
4. License compatibility
5. Performance characteristics

## OpenHands Integration

### Headless Browser Requirements
- Must support Playwright (preferred) or Puppeteer
- Needs to handle authentication securely
- Should manage session persistence
- Must support multiple concurrent connections

### Communication Architecture
1. Primary OpenHands instance for core operations
2. Secondary instance for agent communication
3. Message routing between instances
4. Status monitoring dashboard

### Questions for Implementation:
1. What authentication method should we use for OpenHands instances?
2. Should we implement message encryption between instances?
3. What are the performance requirements for message handling?
4. Should we implement a message queue system between instances?