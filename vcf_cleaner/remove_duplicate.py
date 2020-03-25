class Contact:
    def __init__(self, raw_data, id_contact):
        self.entries = []
        self.data = {}
        self.raw_data = raw_data
        self.id_contact = id_contact

    def convert_key_name(self, key_name):
        dict_conv = {
            "DAVDROID1.EMAIL": "EMAIL",
            "GROUP1.EMAIL": "EMAIL",
            "GROUP2.EMAIL": "EMAIL",
            "DAVDROID2.EMAIL": "EMAIL",
        }
        return dict_conv.get(key_name, key_name).lower()


    def add_entry(self, name, content, line=""):
        self.entries.append((name, line))
        name = self.convert_key_name(name)
        if name in self.data.keys():
            if isinstance(self.data[name], list):
                if not content in self.data[name]:
                    self.data[name].append(content)
            else:
                if not content == self.data[name]:
                    self.data[name] = [self.data[name], content]
        else:
            self.data[name] = content

    def __str__(self):
        return str(self.data.get("fn", "FULL NAME MISSING")) + str(self.data.keys())

    def __repr__(self):
        return str(self.data.get("fn", "FULL NAME MISSING")) + str(self.data.keys())

    def get(self, key_name):
        if key_name in self.data.keys():
            return self.data[key_name]
        else:
            raise KeyError("Key %s doesn't exist in %s" % (key_name, self))

    def print_field(self, key_name):
        data = self.data.get(key_name, [])
        if isinstance(data, list):
            return [
                "%s:%s" % (key_name.upper(), d) for d in data
            ]
        else:
            return ["%s:%s" % (key_name.upper(), data)]


class Contacts:
    def __init__(self):
        self.data = {}

        self.data_name = {}
        self.data_email = {}

        self.mergeable = ["email", "tel"]
        self.to_save = ["fn", "n", "email", "tel", "version"]

    def add_contact(self, contact):
        id_contact = contact.id_contact
        self.data[id_contact] = contact

        to_merge = []
        try:
            name = contact.get("n")
            
            if name in self.data_name.keys():
                print("TO MERGE", id_contact, "and", self.data_name[name])
                to_merge.append(self.data_name[name])
            else:
                self.data_name[name] = id_contact
        except KeyError as e:
            print("Missing name", e)

        try:
            email = contact.get("email")
            if isinstance(email, list):
                for e in email:
                    if e in self.data_email:
                        print("TO MERGE", id_contact, "and", self.data_email[e])
                        to_merge.append(self.data_email[e])
                    else:
                        self.data_email[e] = id_contact
        except KeyError as e:
            pass
            # print("Missing email", e)
        
        to_merge = list(set(to_merge))

        for other in to_merge:
            self.merge_with(id_contact, other)

    def merge_with(self, ref, other):
        for key_name in self.mergeable:# self.data[other].data.items():
            data = self.data[other].data.get(key_name, None)
            if data:
                if isinstance(data, list):
                    for d in data:
                        self.data[ref].add_entry(key_name, d)
                else:
                    self.data[ref].add_entry(key_name, data)
        del self.data[other]

    def __str__(self):
        return str(self.data)

    def save(self):
        out = []
        for contact in self.data.values():
            out.append("BEGIN:VCARD")
            for field in self.to_save:
                out += contact.print_field(field)
            out.append("END:VCARD")
        return "\n".join(out)

        


columns_to_drop = ["PRODID", "UID"]

all_contacts = Contacts()

i = 0

with open("contacts.vcf", "r", encoding="utf-8") as reader:
    file = reader.read().strip().strip("BEGIN:VCARD").strip("END:VCARD").strip()
    contacts = file.split("END:VCARD\nBEGIN:VCARD")
    for contact in contacts:
        print("New contact")
        i += 1
        new_contact = Contact(contact, i)

        fields = contact.strip().split("\n")
        for field in fields:
            if not ":" in field:
                print("\tERROR on", contact)
                continue
            elements = field.split(":")
            name_field = elements[0]
            if ";" in name_field:
                elements_name = name_field.split(";")
                name_field = elements_name[0]
                type_field = elements_name[1]

            content_field = elements[1]
            try:
                new_contact.add_entry(name_field, content_field, field)
            except KeyError as e:
                print("ERROR", e)

        all_contacts.add_contact(new_contact)
        if i > 10:
            break
with open("contacts_out.vcf", "w", encoding="utf-8") as f:
    f.write(all_contacts.save())
