import sys,codecs,os,math,operator
from collections import Counter

def read_from_files(cand, ref):
    references = []
    if '.txt' in ref:
        references.append(codecs.open(ref, 'r', 'utf-8').readlines())
    else:
        for root, dirs, files in os.walk(ref):
            for f in files:
                references.append(codecs.open(os.path.join(root, f), 'r', 'utf-8').readlines())
    candidate = codecs.open(cand, 'r', 'utf-8').readlines()
    return candidate, references

def find_ngrams(input_list, n):
    return [' '.join(x) for x in zip(*[input_list[i:] for i in range(n)])]

def mycount_gram(candidate, references, n):
    count=0
    clipCount=0
    for i in range(len(candidate)):
        reference_counters=[Counter(find_ngrams(x[i].strip().split(), n)) for x in  references]
        candidate_counters=Counter(find_ngrams(candidate[i].strip().split(), n))
        clipCount+=float(myClip_Count(candidate_counters,reference_counters))
        count+=len(candidate[i].strip().split())-n+1
    return clipCount/count

def myClip_Count(cand_d, ref_ds):
    return sum((cand_d&reduce(operator.or_,ref_ds)).values())

def brevity_penalty(c, r):
    if c > r:
        return 1
    return math.exp(1-(float(r)/c))

def calc_brevity_penalty(candidate, references):
    refLens=0
    canLens=0
    for i in range(len(candidate)):
        myreferences=[len(x[i].strip().split()) for x in references]
        mycandidate=len(candidate[i].strip().split())
        canLens+=mycandidate
        refLens+=best_length_match(myreferences,mycandidate)
    return brevity_penalty(canLens,refLens)

def geometric_mean(precisions):
    return (reduce(operator.mul, precisions)) ** (1.0 / len(precisions))

def best_length_match(ref_l, cand_l):
    temp_list=[abs(x-cand_l) for x in ref_l]
    posi,_=min(enumerate(temp_list), key=operator.itemgetter(1))
    return ref_l[posi]

candidate, references = read_from_files(sys.argv[1], sys.argv[2])
myprecisions = []
for i in range(4):
    myprecisions.append(mycount_gram(candidate, references, i+1))
mybleu = geometric_mean(myprecisions) * calc_brevity_penalty(candidate,references)
print mybleu
out = open('bleu_out.txt', 'w')
out.write(str(mybleu))
out.close()