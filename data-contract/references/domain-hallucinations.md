# Domain-Specific Hallucination Targets

Fields that AI code generators (Cursor, Copilot, Claude, Gemini) will plausibly invent for each domain. These are the most common phantom fields observed in AI-generated frontend code.

## Why This Matters

AI models trained on vast codebases have strong priors about what fields "should" exist in a given domain. A healthcare app "should" have `patient_id` and `diagnosis_code`. A finance app "should" have `credit_score`. When generating frontend components, AI will confidently reference these fields even when the backend never sends them.

The negative list in DATA_CONTRACT.md is the firewall. It explicitly tells the AI: "These fields do NOT exist. Do not generate UI for them."

## HLS (Healthcare & Life Sciences)

### Patient Demographics (most common hallucinations)
`patient_id`, `mrn`, `medical_record_number`, `dob`, `date_of_birth`, `age`, `gender`, `sex`, `ethnicity`, `race`, `address`, `phone`, `emergency_contact`, `next_of_kin`, `insurance_id`, `insurance_provider`, `insurance_group`, `copay`, `deductible`

### Clinical Data
`clinical_notes`, `progress_notes`, `discharge_summary`, `history_of_present_illness`, `chief_complaint`, `review_of_systems`, `physical_exam`, `assessment_plan`, `diagnosis`, `diagnosis_code`, `icd10_code`, `icd9_code`, `cpt_code`, `drg`, `hcpcs_code`, `snomed_code`

### Provider/Facility
`provider_npi`, `attending_physician`, `referring_physician`, `facility_id`, `department`, `unit`, `bed_number`, `room_number`, `admission_date`, `discharge_date`, `length_of_stay`

### Lab/Results
`lab_results`, `lab_values`, `vitals`, `blood_pressure`, `systolic`, `diastolic`, `heart_rate`, `respiratory_rate`, `temperature`, `spo2`, `bmi`, `weight`, `height`

### Medications/Allergies
`medications`, `current_medications`, `medication_list`, `allergies`, `allergy_list`, `immunizations`, `vaccination_status`, `adverse_reactions`

### Pathology/Oncology
`staging_info`, `tnm_stage`, `grade`, `biomarkers`, `staining_method`, `stain`, `laterality`, `specimen_type`, `accession_number`, `pathology_report`, `tumor_size`, `margin_status`, `lymph_node_status`, `ki67`, `her2`, `er_status`, `pr_status`

### Genomics
`gene_name`, `variant`, `mutation`, `zygosity`, `allele_frequency`, `clinical_significance`, `acmg_classification`, `rsid`, `chromosome`, `position`, `ref_allele`, `alt_allele`

## FSI (Financial Services)

### Personal/Account
`ssn`, `social_security`, `tax_id`, `ein`, `account_number`, `routing_number`, `iban`, `swift_code`, `account_balance`, `available_balance`, `pending_transactions`

### Credit/Risk
`credit_score`, `fico_score`, `credit_limit`, `apr`, `interest_rate`, `debt_to_income`, `payment_history`, `delinquency_count`, `days_past_due`, `charge_off_amount`, `risk_score`, `risk_rating`, `probability_of_default`

### Investment
`portfolio_value`, `asset_allocation`, `unrealized_gains`, `realized_gains`, `dividend_yield`, `expense_ratio`, `sharpe_ratio`, `beta`, `alpha`, `nav`, `aum`

### Compliance
`kyc_status`, `kyc_date`, `aml_flag`, `sanctions_match`, `pep_status`, `suspicious_activity`, `sar_filed`, `ctr_filed`, `beneficial_owner`

### Income/Employment
`annual_income`, `monthly_income`, `employment_status`, `employer_name`, `job_title`, `years_employed`

## Retail / E-Commerce

### Customer
`purchase_history`, `order_history`, `lifetime_value`, `clv`, `customer_segment`, `loyalty_points`, `loyalty_tier`, `referral_code`, `referral_count`

### Engagement
`cart_abandonment_rate`, `session_duration`, `pages_per_session`, `bounce_rate`, `click_through_rate`, `conversion_rate`, `email_open_rate`, `nps_score`, `csat_score`

### Product
`inventory_count`, `stock_status`, `reorder_point`, `supplier`, `cost_price`, `margin`, `return_rate`, `defect_rate`

### Subscription
`subscription_tier`, `subscription_start`, `subscription_end`, `churn_probability`, `monthly_recurring_revenue`, `annual_recurring_revenue`

## IoT / Manufacturing

### Device
`device_firmware`, `firmware_version`, `hardware_version`, `serial_number`, `mac_address`, `ip_address`, `device_type`, `manufacturer`, `model_number`

### Telemetry
`battery_level`, `signal_strength`, `rssi`, `snr`, `uptime`, `last_heartbeat`, `operating_temperature`, `humidity`, `vibration`, `power_consumption`

### Maintenance
`calibration_date`, `next_calibration`, `maintenance_schedule`, `last_maintenance`, `mtbf`, `mttr`, `failure_mode`, `failure_count`, `warranty_expiry`

### Industrial
`anomaly_score`, `oee`, `throughput`, `cycle_time`, `defect_rate`, `scrap_rate`, `downtime_minutes`, `geofence_status`

## General (Always Include)

### Audit/Metadata
`created_by`, `created_at`, `updated_by`, `updated_at`, `deleted_at`, `is_deleted`, `version`, `revision`, `audit_trail`, `change_log`

### Auth/Permissions
`permissions`, `roles`, `access_level`, `tenant_id`, `org_id`, `api_key`, `api_secret`, `access_token`, `refresh_token`

### Session/Tracking
`last_login`, `login_count`, `ip_address`, `user_agent`, `session_token`, `session_id`, `fingerprint`, `device_id`

## Usage Notes

1. **Filter before including**: Compare each hallucination target against the actual schema. Only include fields that are plausible but ABSENT.
2. **Add project-specific entries**: The user knows their domain best. Always ask them to review and add/remove entries.
3. **Update when schema changes**: If the backend adds a field that was previously in the negative list, remove it from the negative list and add it to the positive list.
4. **Cross-dataset confusion**: AI will often confuse related but different datasets (e.g., LC25000 vs TCGA, MIMIC vs eICU). Add dataset-specific clarifications to interpretation rules.
