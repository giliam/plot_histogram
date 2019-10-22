class Contact:
    def __init__(self, raw_data):
        self.entries = []
        self.raw_data = raw_data

    def add_entry(self, line):
        self.entries.append(line)

columns_to_drop = ["PRODID", "UID"]

with open("contacts.vcf", "r", encoding="utf-8") as reader:
    file = reader.read().strip().strip("BEGIN:VCARD\n").strip("END:VCARD")
    contacts = file.split("END:VCARD\nBEGIN:VCARD")
    for contact in contacts:
        new_contact = Contact(contact)

        fields = contact.strip().split("\n")
        for field in fields:
            if not ":" in field:
                print("ERROR on", contact)
                continue
            elements = field.split(":")
            name_field = elements[0]
            content_field = elements[1]
            print("Field", name_field, "with content", content_field)
        break
