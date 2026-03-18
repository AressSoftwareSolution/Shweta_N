import re
text="Maria Johnson recently @ joined our team as # a project coordinator. You can reach her at maria.johnson@example.com for any $ queries related ] to scheduling. For urgent matters, feel free to call her directly at +1-202-555-0147 during office hours."

## Lowercase the text
Lw_text=text.lower()

## extracting email
pattern="[a-zA-Z0-9._]+@[a-zA-Z0-9._]+\.[a-zA-Z0-9]{2,}"
email=re.search(pattern,text)
print("Email:",email.group())

## extracting phone number
ph_pattern=r"\+\d{1,9}-\d{3}-\d{3}-\d{4}" ## +1-202-555-0147 for indian number the pattern will be \+\d{1,9}-\d{5}-\d{5}
phone_no=re.search(ph_pattern,text)
print("Phone Number:",phone_no.group())

## Removing special characters
clean_text=re.sub(r'[^\w\s]','',text)

## Removing Extra Spaces
clean_text=re.sub("\s+"," ",clean_text)

## Spliting the Text into words 
words=clean_text.split()
print("Splited Words:",words)

print(f"Processed Text:{clean_text}")

## Storing Extracted infromation in dic
extracted_info={
    "email": email.group(),
    "phone_number":phone_no.group(),
}
print("Extracted Information:",extracted_info)

print("clean Text:",clean_text)

with open("data.txt", "w") as f:
    f.write(clean_text)
