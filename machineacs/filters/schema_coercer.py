from typing import Any, Dict, Generator, Iterable
import unicodedata

from filters.tokens import Token, StringValueToken, KeyToken, NumberToken, BoolNullToken, RuleToken

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

# Variations of null values
NULL_VARIATIONS = ["", "Unknown", "N/A", "NA", "n/a", "na", "None", "none", "NONE", "null", "Null", "NULL"]

# 2. Build a Reverse Lookup Map (Variation -> Standard Key) for fast, O(1) lookup
REVERSE_MAP = {}
for standard_key, variations in KEY_VARIATIONS.items():
    for var in variations:
        REVERSE_MAP[var] = standard_key


def coerce_schema(tokens: Iterable[Token]) -> Generator[Token, None, None]:
    """
    A stateful generator that maps keys and coerces following values
    according to a predefined standard schema.
    """
    current_key = None
    
    for token in tokens:
        
        # 3. Standardize Keys
        if isinstance(token, KeyToken):
            original_key = token.content
            standard_key = REVERSE_MAP.get(original_key, original_key)
            
            if original_key != standard_key:
                # Yield an Audit Rule Token
                yield RuleToken({
                    "rule_type": "Key Standardization",
                    "before": original_key,
                    "after": standard_key
                })
            
            # Update our state machine
            current_key = standard_key
            yield KeyToken(standard_key)
            continue
            
        # 4. Canonicalize Values based on Standard Keys
        elif type(token) in (StringValueToken, NumberToken, BoolNullToken):
            value = token.content
            original_type = type(value).__name__
            
            # Null Check
            if value in NULL_VARIATIONS or value is None:
                if value is not None:
                    yield RuleToken({
                        "rule_type": "Null Standardization",
                        "before": str(value),
                        "after": "null"
                    })
                yield BoolNullToken(None)
                continue
            
            # Type Coercion
            try:
                coerced_value = value
                
                if current_key in ["employee_id", "age"]:
                    coerced_value = int(float(value))
                    if isinstance(coerced_value, int):
                        yield NumberToken(coerced_value)
                        
                elif current_key == "salary":
                    if isinstance(value, str):
                        value = value.replace("$", "").replace(",", "")
                    coerced_value = round(float(value), 3)
                    yield NumberToken(coerced_value)
                        
                elif current_key == "is_active":
                    if isinstance(value, str):
                        coerced_value = value.lower() in ("true", "1", "yes")
                    else:
                        coerced_value = bool(value)
                    yield BoolNullToken(coerced_value)
                        
                elif current_key in ["email", "full_name", "city", "job_title", "department", "country"]:
                    val_str = str(value).strip()
                    coerced_value = unicodedata.normalize("NFC", val_str)
                    yield StringValueToken(coerced_value)
                else:
                    # Pass through unknown keys
                    yield token
                    continue
                
                # If we successfully coerced and the type or string exact representation changed
                if str(value) != str(coerced_value) or type(value) != type(coerced_value):
                    yield RuleToken({
                        "rule_type": "Type Coercion",
                        "key": current_key,
                        "before": f"{value} ({original_type})",
                        "after": f"{coerced_value} ({type(coerced_value).__name__})"
                    })
                    
            except (ValueError, TypeError):
                # If coercion fails, yield the original token
                yield token
        
        else:
            # Pass through structural tokens (}, {, [, ], etc.) unmodified
            yield token
