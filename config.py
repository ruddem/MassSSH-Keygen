description = "Tool to generate encrypted SSH-Keys\nFollowing output for every SSH-Key-Pair:\n .ppk, .pub, .key, .pass\n(.pass contains password for the encrypted private-key)"
generated_files_location = "keys/"
keys_to_generate = 1
dry_run = False
key_type = "ed25519"
parallel_threads = 1