def order(sentence):
  return ' '.join(sorted(sentence.split(' '), key=lambda x: sorted(x)))
