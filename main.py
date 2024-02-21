import argparse
import secrets
import string
from datetime import datetime
import hashlib
from multiprocessing import Process
import multiprocessing as mp

import config
import modules.shell_execute as shell_execute
import modules.init as init


def main():
    parser = argparse.ArgumentParser(description=config.description)

    parser.add_argument("-l", "--generated_files_location", dest="generated_files_location", default=config.generated_files_location, help = "Define save location for generated Files (default='" + config.generated_files_location + "')")
    parser.add_argument("-g", "--keys_to_generate", dest="keys_to_generate", default=config.keys_to_generate, type=int, help = "Define number of keys to generate (default='" + str(config.keys_to_generate) + "')")
    parser.add_argument("-d", "--dry", dest="dry_run", default=config.dry_run, choices=['True', 'False'], help = "dry run script, only print in cli (default='" + str(config.dry_run) + "')")
    parser.add_argument("-t", "--key_type", dest="key_type", default=config.key_type, choices=['ed25519', 'rsa'], help = "specify key type when generating (ed25519, rsa) (default='" + str(config.key_type) + "')")
    parser.add_argument("-p", "--parallel_threads", dest="parallel_threads", default=config.parallel_threads, type=int, help = "specify number of prallel threads (default='" + str(config.parallel_threads) + "')")

    args = vars(parser.parse_args())
    generated_files_location = args["generated_files_location"]
    if generated_files_location[-1] != "/":
        generated_files_location = generated_files_location + "/"
    init.make_dirs(generated_files_location)
    keys_to_generate = args["keys_to_generate"]
    dry_run = args["dry_run"]
    key_type = args["key_type"]
    parallel_threads = args["parallel_threads"]

    processes = 1
    if keys_to_generate < parallel_threads:
        pool = mp.Pool(keys_to_generate)
        jobs = []
        for key in range(keys_to_generate):
            job = pool.apply_async(generate_ssh_keys, (generated_files_location, 1, dry_run, key_type,))
            jobs.append(job)
        for job in jobs:
            job.get()

        pool.close()
        pool.join()

    else:
        keys_to_generate_per_thread = keys_to_generate / parallel_threads
        pool = mp.Pool(parallel_threads)
        jobs = []
        for key in range(parallel_threads):
            job = pool.apply_async(generate_ssh_keys, (generated_files_location, keys_to_generate_per_thread, dry_run, key_type,))
            jobs.append(job)

        for job in jobs:
            job.get()

        pool.close()
        pool.join()

        if not keys_to_generate_per_thread.is_integer():
            frac = keys_to_generate_per_thread % 1
            generate_ssh_keys(generated_files_location, frac * parallel_threads, dry_run, key_type)


def generate_ssh_keys(generated_files_location, keys_to_generate, dry_run, key_type):
    i = 1
    while i <= keys_to_generate:
        now = datetime.now()
        timestamp = str(int(datetime.timestamp(now)))
        timestamp_hash = hashlib.sha256(timestamp.encode()).hexdigest()
        alphabet = string.ascii_letters + string.digits + "!#()"
        date_today = now.strftime("%Y%m%d")
        timestamp_hash = ''.join(secrets.choice(timestamp_hash) for i in range(16))
        password = ''.join(secrets.choice(alphabet) for i in range(20))
        key_name = str(date_today + "_" + timestamp_hash)
        pass_file_name = key_name + ".pass"

        if not dry_run:
            shell_execute.write_pass_file(generated_files_location, password, pass_file_name)
            shell_execute.keygen(generated_files_location, key_name, pass_file_name, key_type)
            shell_execute.write_fingerprint_file(generated_files_location, key_name)
            print("Generated", key_name)

        else:
            print('-' * 50)
            print("Dry Run for Key:", key_name)
            print("Generated Files Location:", generated_files_location)
            print("Pass-Filename:", pass_file_name, "Pass-Content:", password)
            print("Key-Name:", key_name)

        password = ""
        pass_file_name = ""
        key_name = ""
        i = i + 1


if __name__ == "__main__":
    main()
