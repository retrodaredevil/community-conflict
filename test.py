import snap

FILENAME = "/data/soc-redditHyperlinks-body.tsv"

context = snap.TTableContext()

schema = snap.Schema()
schema.Add(snap.TStrTAttrPr("Source", snap.atStr))
schema.Add(snap.TStrTAttrPr("Target", snap.atStr))
schema.Add(snap.TStrTAttrPr("PostId", snap.atStr))
schema.Add(snap.TStrTAttrPr("Timestamp", snap.atStr))
#schema.Add(snap.TStrTAttrPr("LinkSentiment", snap.atInt))
schema.Add(snap.TStrTAttrPr("LinkSentiment", snap.atStr))
schema.Add(snap.TStrTAttrPr("Properties", snap.atStr))

# https://snap.stanford.edu/snappy/doc/reference/table.html
table = snap.TTable.LoadSS(schema, FILENAME, context, "\t", snap.TBool(False))

