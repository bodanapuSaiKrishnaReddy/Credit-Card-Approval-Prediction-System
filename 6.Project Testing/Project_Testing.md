# Phase 6: Project Testing

## 🧪 Test Execution Details
We run 8 comprehensive unit tests covering endpoints, validation constraints, and page routing:

```powershell
python tests.py
```

### Test Suite Output:
```
........
----------------------------------------------------------------------
Ran 8 tests in 0.090s

OK
```

### Validated Test Cases:
1. **Home Page**: Confirms landing page loads with the `Credit Card Prediction` header.
2. **About Page**: Verifies policies and guidelines route.
3. **Inquiries Page**: Checks dynamic data binding.
4. **Reports Page**: Validates real-time calculations.
5. **Custom 404 Handler**: Enforces page-not-found handler matches branding.
6. **Form Validation**: Assures Pydantic schema catches missing features.
7. **Safe Fallback**: Confirms unseen data values abort with HTTP 400 validation messages.
