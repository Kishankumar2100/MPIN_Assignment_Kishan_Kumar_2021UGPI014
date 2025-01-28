import streamlit as st
import random

def check_demographics(dob, anniversary, spouse_dob, mpin):
    reasons = []
    
    dob_parts = [
        dob[:2],  
        dob[3:5],  
        dob[6:],  
    ]
    anniversary_parts = [
        anniversary[:2],  
        anniversary[3:],  
    ]
    spouse_dob_parts = [
        spouse_dob[:2], 
        spouse_dob[3:5],  
        spouse_dob[6:],  
    ]
    
    if any(part in mpin for part in dob_parts):
        reasons.append("DEMOGRAPHIC_DOB_SELF")
    if any(part in mpin for part in anniversary_parts):
        reasons.append("DEMOGRAPHIC_ANNIVERSARY")
    if any(part in mpin for part in spouse_dob_parts):
        reasons.append("DEMOGRAPHIC_DOB_SPOUSE")
    
    return reasons

def check_common_patterns(mpin):
    common_pins = {
        '1234', '1111', '0000', '2222', '4321', '9876', '5555', '1212', '1001',
        '123456', '111111', '222222', '333333', '123123', '654321', '777777'
    }
    if mpin in common_pins:
        return True, ["COMMONLY_USED"]
    return False, []

def check_repeated_digits(mpin):
    if len(set(mpin)) == 1:  
        return True, ["REPEATED_DIGITS"]
    return False, []

def check_pin_strength(mpin, dob, anniversary, spouse_dob):
    is_common, common_reasons = check_common_patterns(mpin)
    is_repeated, repeated_reasons = check_repeated_digits(mpin)
    reasons = common_reasons + repeated_reasons

    if is_common or is_repeated:
        return "WEAK", reasons
    
    demographic_reasons = check_demographics(dob, anniversary, spouse_dob, mpin)
    reasons += demographic_reasons
    
    if reasons:
        return "WEAK", reasons
    else:
        return "STRONG", []

def run_test_cases():
    test_cases = [
        {"pin": "1111", "dob": "13031998", "anniversary": "0101", "spouse_dob": "04011997", "expected_strength": "WEAK"},
        {"pin": "1234", "dob": "05051990", "anniversary": "0303", "spouse_dob": "06061992", "expected_strength": "WEAK"},
        {"pin": "9876", "dob": "29061989", "anniversary": "2512", "spouse_dob": "04101994", "expected_strength": "WEAK"},
        {"pin": "0000", "dob": "02081995", "anniversary": "1407", "spouse_dob": "12121996", "expected_strength": "WEAK"},
        {"pin": "2222", "dob": "09051992", "anniversary": "1508", "spouse_dob": "08011993", "expected_strength": "WEAK"},
        {"pin": "4321", "dob": "25081991", "anniversary": "1111", "spouse_dob": "15041990", "expected_strength": "WEAK"},
        {"pin": "5555", "dob": "03031996", "anniversary": "0210", "spouse_dob": "10011997", "expected_strength": "WEAK"},
        {"pin": "1212", "dob": "12051994", "anniversary": "2206", "spouse_dob": "03081993", "expected_strength": "WEAK"},
        {"pin": "1357", "dob": "16071988", "anniversary": "1006", "spouse_dob": "22031989", "expected_strength": "STRONG"},
        {"pin": "2468", "dob": "01061990", "anniversary": "0305", "spouse_dob": "17021992", "expected_strength": "STRONG"},
        {"pin": "8434", "dob": "19051989", "anniversary": "1207", "spouse_dob": "03011990", "expected_strength": "STRONG"},
        {"pin": "7632", "dob": "28081993", "anniversary": "1011", "spouse_dob": "25061994", "expected_strength": "STRONG"},
        {"pin": "0000", "dob": "22061988", "anniversary": "1409", "spouse_dob": "12121989", "expected_strength": "WEAK"},
        {"pin": "8008", "dob": "11051991", "anniversary": "1502", "spouse_dob": "04081992", "expected_strength": "STRONG"},
        {"pin": "9276", "dob": "03061985", "anniversary": "0705", "spouse_dob": "09041986", "expected_strength": "STRONG"},
        {"pin": "2125", "dob": "21071994", "anniversary": "2512", "spouse_dob": "06121995", "expected_strength": "WEAK"},
        {"pin": "1234", "dob": "16031992", "anniversary": "0508", "spouse_dob": "10081993", "expected_strength": "WEAK"},
        {"pin": "3472", "dob": "02041990", "anniversary": "2306", "spouse_dob": "15081991", "expected_strength": "STRONG"},
        {"pin": "3456", "dob": "07021986", "anniversary": "1804", "spouse_dob": "24091987", "expected_strength": "WEAK"},
        {"pin": "5198", "dob": "12081995", "anniversary": "0910", "spouse_dob": "18031996", "expected_strength": "STRONG"},
        {"pin": "123456", "dob": "07071985", "anniversary": "2006", "spouse_dob": "15041987", "expected_strength": "WEAK"},
        {"pin": "654321", "dob": "18121980", "anniversary": "0404", "spouse_dob": "21101982", "expected_strength": "WEAK"},
        {"pin": "000001", "dob": "14011990", "anniversary": "0404", "spouse_dob": "23061992", "expected_strength": "STRONG"},
        {"pin": "111111", "dob": "21061985", "anniversary": "0912", "spouse_dob": "11081986", "expected_strength": "WEAK"},
        {"pin": "456789", "dob": "13031980", "anniversary": "0906", "spouse_dob": "25111983", "expected_strength": "WEAK"},
        {"pin": "789123", "dob": "17021988", "anniversary": "2204", "spouse_dob": "03081985", "expected_strength": "STRONG"},
        {"pin": "254678", "dob": "12071992", "anniversary": "0511", "spouse_dob": "16091989", "expected_strength": "STRONG"},
        {"pin": "984235", "dob": "25081990", "anniversary": "1807", "spouse_dob": "29061989", "expected_strength": "STRONG"},
        {"pin": "678234", "dob": "05101995", "anniversary": "1210", "spouse_dob": "01011996", "expected_strength": "STRONG"},
        {"pin": "342561", "dob": "28071996", "anniversary": "0202", "spouse_dob": "14081997", "expected_strength": "WEAK"},
        {"pin": "543821", "dob": "15101987", "anniversary": "0309", "spouse_dob": "07111988", "expected_strength": "STRONG"},
        {"pin": "251504", "dob": "04121988", "anniversary": "1507", "spouse_dob": "25011990", "expected_strength": "WEAK"},
        {"pin": "900631", "dob": "11081989", "anniversary": "2204", "spouse_dob": "15061992", "expected_strength": "STRONG"},
        {"pin": "987654", "dob": "05051991", "anniversary": "2309", "spouse_dob": "06031993", "expected_strength": "WEAK"},
        {"pin": "345678", "dob": "21021990", "anniversary": "1905", "spouse_dob": "17081992", "expected_strength": "WEAK"},
        {"pin": "843492", "dob": "02061985", "anniversary": "1207", "spouse_dob": "24021986", "expected_strength": "STRONG"},
        {"pin": "123456", "dob": "15031987", "anniversary": "0802", "spouse_dob": "05101988", "expected_strength": "WEAK"},
        {"pin": "111111", "dob": "07101980", "anniversary": "0612", "spouse_dob": "22031982", "expected_strength": "WEAK"},
        {"pin": "222310", "dob": "29011992", "anniversary": "0405", "spouse_dob": "17101993", "expected_strength": "STRONG"},
        {"pin": "111222", "dob": "23071990", "anniversary": "1104", "spouse_dob": "25081991", "expected_strength": "WEAK"},
        
    ]
    
    for i, test_case in enumerate(test_cases):
        pin = test_case["pin"]
        dob = test_case["dob"]
        anniversary = test_case["anniversary"]
        spouse_dob = test_case["spouse_dob"]
        expected_strength = test_case["expected_strength"]
        
        strength, reasons = check_pin_strength(pin, dob, anniversary, spouse_dob)
        
        if strength != expected_strength:
            st.error(f"Test case {i+1} failed! Expected {expected_strength} but got {strength}")
        else:
            st.success(f"Test case {i+1} passed! MPIN: {pin}, Strength: {strength}")

def main():
    st.title("MPIN Strength Checker")
    
    st.sidebar.header("Enter Your Demographics")
    dob = st.sidebar.text_input("Enter your Date of Birth (DDMMYYYY or DDMM)", "")
    anniversary = st.sidebar.text_input("Enter your Wedding Anniversary (DDMM)", "")
    spouse_dob = st.sidebar.text_input("Enter your Spouse's Date of Birth (DDMMYYYY or DDMM)", "")
    
    mpin = st.text_input("Enter your MPIN (4 or 6 digits)", "")
    
    if st.button("Check MPIN Strength"):
        if dob and anniversary and spouse_dob and mpin:
            strength, reasons = check_pin_strength(mpin, dob, anniversary, spouse_dob)
            
            st.write(f"MPIN Strength: **{strength}**")
            
            if strength == "WEAK":
                st.write("Reasons for weakness:")
                for reason in reasons:
                    st.write(f"- {reason}")
        else:
            st.error("Please fill in all fields!")
    
    if st.button("Run Automated Tests"):
        run_test_cases()

if __name__ == "__main__":
    main()
