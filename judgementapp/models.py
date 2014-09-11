from django.conf import settings
from django.db import models
from BeautifulSoup import BeautifulSoup as Soup

# Create your models here.


class Document(models.Model):
    docId = models.CharField(max_length=250)
    text = models.TextField()

    def __unicode__(self):
        return self.docId

    def get_content(self):
        content = ""

        # need to query SQLite DB for the format
        # SELECT format FROM judgementapp_document WHERE docID=' + self.docID + '
        file_type = ""

        if file_type == "html":
            try:
                with open(settings.DATA_DIR + "/" + self.docId) as f:
                    content = f.read()
            except Exception:
                content = "Could not read html file %s" % settings.DATA_DIR + "/" + self.docId
        elif file_type == "trec":
            try:
                with open(settings.DATA_DIR + "/" + self.docId) as f:
                    content = f.read()

                    #this is an implementation for trectxt
                    soup = Soup(content)
                    for doc in soup.findAll('doc'):
                        doc_no = doc.find('docno')
                        text = doc.find('text')
                        content = "<h5>" + doc_no + "</h5><p>" + text + "</p>"

            except Exception:
                content = "Could not read trrec file %s" % settings.DATA_DIR + "/" + self.docId
        else:
            content = "Unknown format encountered, document parser failed."

        return content


class Query(models.Model):
    qId = models.IntegerField()
    text = models.CharField(max_length=250)
    difficulty = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    instructions = models.TextField(blank=True, null=True)
    criteria = models.TextField(blank=True, null=True)
    example = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return '%s: %s' % (self.qId, self.text)

    def num_unjudged_docs(self):
        unjugded = [judgement for judgement in self.judgements() if judgement.relevance < 0]
        return len(unjugded)

    def num_judgements(self):
        return len(self.judgements())

    def judgements(self):
        return Judgement.objects.filter(query=self.id)


class Judgement(models.Model):
    labels = {-1: 'Unjudged', 0: 'Not relvant', 1: 'Somewhat relevant', 2: 'Highly relevant'}

    query = models.ForeignKey(Query)
    document = models.ForeignKey(Document)
    comment = models.TextField(blank=True, null=True)

    relevance = models.IntegerField()

    def __unicode__(self):
        return '%s\t0%s\t%s\n' % (self.query.qId, self.document.docId, self.relevance)


    def label(self):
        return self.labels[self.relevance]
