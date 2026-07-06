# Phase 2: Requirement Analysis

## 📋 Functional Requirements
1. **Multi-step Form (Wizard)**: Applicants should be able to submit their information across 3 logical steps:
   - Step 1: Personal Details (Name, Age, Gender, Family Size, Phone, Email)
   - Step 2: Financial Assets (Annual Income, Car ownership, Realty ownership, Housing Type)
   - Step 3: Employment Info (Income type, Occupation, Work Experience, Education)
2. **Interactive Review**: Users must review all details before submitting. Checks must be in place to ensure details are validated.
3. **Real-time Assessment**: Evaluates the model prediction dynamically and redirects to a color-coded outcome page.
4. **Dashboard Views**:
   - **Inquiries**: Lists all evaluated applicants dynamically with a "View File" modal to inspect variables.
   - **Reports**: Displays real-time operational analytics (KPIs, approval rate distributions by income tiers).

## ⚙️ Non-Functional Requirements
1. **High Classification Accuracy**: The predictor model must maintain > 85% accuracy on test splits.
2. **Input Sanitation & Protection**:
   - Pydantic schema verification for format validation.
   - Safe category rejection mapping to prevent server crashes on unseen data inputs.
3. **Responsive Visual System**: Fully optimized layout for mobile, tablet, and desktop viewports.
