import itertools
import zipfile

def gather_user_info():
    user_info = {}
    user_info['first_name'] = input("Enter your first name: ")
    user_info['last_name'] = input("Enter your last name: ")
    user_info['birth_year'] = input("Enter your birth year: ")
    user_info['birth_month'] = input("Enter your birth month: ")
    user_info['birth_day'] = input("Enter your birth day: ")
    user_info['pet_name'] = input("Enter your pet's name: ")
    user_info['favorite_color'] = input("Enter your favorite color: ")
    return user_info

def generate_password_list(user_info):
    base_words = list(user_info.values())
    password_list = set()

    password_list.update(base_words)

    for combination in itertools.combinations(base_words, 2):
        password_list.add(''.join(combination))
        password_list.add(''.join(combination[::-1]))

    for combination in itertools.combinations(base_words, 3):
        password_list.add(''.join(combination))
        password_list.add(''.join(combination[::-1]))

    special_chars = ['!', '@', '#', '$', '%']
    for word in base_words:
        for num in range(10):
            password_list.add(f"{word}{num}")
            password_list.add(f"{num}{word}")
        for char in special_chars:
            password_list.add(f"{word}{char}")
            password_list.add(f"{char}{word}")

    return list(password_list)

def save_passwords_to_file(password_list, filename='password_list.txt'):
    with open(filename, 'w') as f:
        for password in password_list:
            f.write(password + '\n')
    print(f"Password list saved to {filename}")

def load_passwords_from_file(filename):
    with open(filename, 'r') as f:
        password_list = [line.strip() for line in f]
    return password_list

def brute_force_zip(password_list, zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zfile:
        for password in password_list:
            try:
                zfile.extractall(pwd=bytes(password, 'utf-8'))
                print(f"Password found: {password}")
                return password
            except (RuntimeError, zipfile.BadZipFile, zipfile.LargeZipFile):
                continue
    print("Password not found.")
    return None

def main():
    print("Password Cracking Tool")
    print("1. File-Based Brute Force")
    print("2. Create Password Text File")
    
    choice = input("Select an option (1/2): ")

    if choice == '1':
        use_existing = input("Do you want to use an existing password file? (yes/no): ").strip().lower()
        if use_existing == 'yes':
            password_file = input("Enter the path to the existing password file: ").strip()
            password_list = load_passwords_from_file(password_file)
        else:
            user_info = gather_user_info()
            password_list = generate_password_list(user_info)
        zip_file_path = input("Enter the path to the zip file: ").strip()
        brute_force_zip(password_list, zip_file_path)
    elif choice == '2':
        user_info = gather_user_info()
        password_list = generate_password_list(user_info)
        filename = input("Enter the filename to save the password list: ").strip()
        save_passwords_to_file(password_list, filename)
    else:
        print("Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    main()
