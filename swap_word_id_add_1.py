
ID_WORD = 'id_word.txt'
WORD_ID = 'word_id.txt'

word_id = open(WORD_ID)
id_word = open(ID_WORD, 'w')
lst = []
for line in word_id:
  line = line.strip().split('\t')
  lst.append((int(line[1])+1, line[0]))

lst = sorted(lst, key=lambda x:x[0])
for (d, w) in lst:
  id_word.write('%d\t%s\n' % (d, w))

word_id.close()
id_word.close()


