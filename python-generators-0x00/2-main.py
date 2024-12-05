#!/usr/bin/python3
import sys
batch_processing = __import__('1-batch_processing').batch_processing

##### print processed users in a batch of 50
try:
    for user in batch_processing(50):
        print(user)
except BrokenPipeError:
    sys.stderr.close()
