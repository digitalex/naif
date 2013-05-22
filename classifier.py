from collections import defaultdict

class Classifier(object):
    def __init__(self):
        self.featurecounts = defaultdict(lambda: defaultdict(int))
        self.doccounts = defaultdict(int)
        self.totalcount = 0

    # Add training data. 'document' is an iterable of features.
    def train(self, document, category):
        for feature in document:
            self.featurecounts[feature].setdefault(category, 0)
            self.featurecounts[feature][category] += 1

        self.doccounts[category] += 1
        self.totalcount += 1

    # Classify a document
    def classify(self, document, default=None):
        best, highest = default, 0.0
        probs = defaultdict(int)

        for category in self.doccounts.iterkeys():
            probs[category] = self.__prob(document, category)
            if probs[category] > highest:
                best, highest = category, probs[category]

        return best

    def __fprob(self, feature, category):
        cc = float(self.doccounts[category])
        fc = float(self.featurecounts[feature][category])
        return fc / cc if cc else 0

    def __weightedprob(self, feature, category, weight=1.0, assumed=0.5):
        basicprob = self.__fprob(feature, category)
        totals = sum(self.featurecounts[feature].itervalues())
        return ((weight * assumed) + (totals * basicprob)) / (weight + totals)

    def __docprob(self, document, category):
        return reduce(lambda p, f: p * self.__weightedprob(f, category), document, 1.0)

    def __prob(self, document, category):
        catprob = self.doccounts[category] / float(self.totalcount)
        docprob = self.__docprob(document, category)
        return catprob * docprob

    def sampletrain(self):
        self.train('nobody owns the water'.split(),'good')
        self.train('the quick rabbit jumps fences'.split(),'good')
        self.train('buy pharmaceuticals now'.split(),'bad')
        self.train('make quick money at the online casino'.split(),'bad')
        self.train('the quick brown fox jumps'.split(),'good')
