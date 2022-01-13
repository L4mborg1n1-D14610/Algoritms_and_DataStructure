import sys

test_file = open(sys.argv[1], 'r')
a = 0
for line in test_file:
    try:
        a += int(line)
        a = a % 256
    except:
        print('')
  #  if line.strip().isnumeric():
 #     a += int(line)
  #      a = a % 256
test_file.close()

answer_file = open(sys.argv[2], 'w')
answer_file.write(str(a))
answer_file.close()
