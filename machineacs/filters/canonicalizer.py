import json
import unicodedata
from typing import Dict, Any
import re

# 1. Map Standard Key -> List of Possible Variations
KEY_VARIATIONS = {
    "employee_id": ["employee_id", "Employee ID", "Employee_ID", "employeeId", "EmployeeId", "EmployeeID", "emp_id", "Emp_ID", "EmpId", "EmpID", "empId"],
    "is_active": ["is_active", "Is Active", "Is_Active", "isActive", "IsActive", "active", "Active", "ACTIVE"],
    "salary": ["salary", "Salary", "SALARY", "sal", "Sal", "SAL", "pay", "Pay", "PAY", "compensation", "Compensation", "COMPENSATION"],
    "email": ["email", "Email", "EMAIL", "e-mail", "E-mail", "E-MAIL", "mail", "Mail", "MAIL"],
    "full_name": ["full_name", "Full Name", "Full_Name", "fullName", "FullName", "name", "Name", "NAME", "first_name", "First Name", "First_Name", "firstName", "FirstName", "last_name", "Last Name", "Last_Name", "lastName", "LastName"],
    "age": ["age", "Age", "AGE"],
    "city": ["city", "City", "CITY"],
    "job_title": ["job_title", "Job Title", "Job_Title", "jobTitle", "JobTitle", "title", "Title", "TITLE"],
    "department": ["department", "Department", "DEPARTMENT", "dept", "Dept", "DEPT"],
    "country": ["country", "Country", "COUNTRY"]
}

#variations of null values
NULL_VARIATIONS = ["", "Unknown", "N/A", "NA", "n/a", "na", "None", "none", "NONE", "null", "Null", "NULL"]

# 2. Build a Reverse Lookup Map (Variation -> Standard Key) for fast, O(1) lookup
REVERSE_MAP = {}
for standard_key, variations in KEY_VARIATIONS.items():
    for var in variations:
        REVERSE_MAP[var] = standard_key


def canonicalize(data_dict: Dict[str, Any]) -> str:
    
    # 3. Standardize Keys
    normalized_data = {}
    for key, value in data_dict.items():
        # Look up the key in our reverse map, if it doesn't exist, keep the original key
        standard_key = REVERSE_MAP.get(key, key)
        normalized_data[standard_key] = value


    # 4. Canonicalize Values based on Standard Keys
    for key, value in list(normalized_data.items()):
        if value in NULL_VARIATIONS:
            normalized_data[key] = None
            continue
            
        # Try to coerce types
        try:
            if key in ["employee_id", "age"]:
                normalized_data[key] = int(float(value))  # float first to catch "32.0"
            elif key == "salary":
                if isinstance(value, str):
                    value = value.replace("$", "").replace(",", "")
                normalized_data[key] = round(float(value), 3)
            elif key == "is_active":
                if isinstance(value, str):
                    normalized_data[key] = value.lower() in ("true", "1", "yes")
                else:
                    normalized_data[key] = bool(value)
            elif key in ["email", "full_name", "city", "job_title", "department", "country"]:
                val_str = str(value).strip()
                # Normalize Unicode (e.g., matching Montréal and Montréal)
                normalized_data[key] = unicodedata.normalize("NFC", val_str)
        except (ValueError, TypeError):
            # If type coercion fails (e.g. converting "Unknown" to float), keep original value
            pass
    
    # 5. Output deterministic JSON
    return json.dumps(normalized_data, sort_keys=True, ensure_ascii=False)




    