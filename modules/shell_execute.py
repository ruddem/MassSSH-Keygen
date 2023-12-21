import os


def write_pass_file(generated_files_location, password, pass_file_name):
    command = "echo '" + password + "' > " + generated_files_location + pass_file_name + ""
    password = ""
    pass_file_name = ""
    os.system(command)
    command = ""
    generated_files_location = ""


def keygen(generated_files_location, key_name, pass_file_name, key_type):
    pass_file_name = generated_files_location + pass_file_name
    key_name = generated_files_location + key_name

    command = "puttygen -t " + key_type + " -C '" + key_name + "' -o " + key_name + ".ppk" \
                     " --new-passphrase " + pass_file_name + " -O private && puttygen" \
                     " " + key_name + ".ppk -O private-openssh --old-passphrase " + pass_file_name + "" \
                     " --new-passphrase " + pass_file_name + " -o " + key_name + ".key && puttygen" \
                     " " + key_name + ".ppk -L -o " + key_name + ".pub"
    key_name = ""
    pass_file_name = ""
    os.system(command)
    command = ""
    generated_files_location = ""
    key_type = ""
