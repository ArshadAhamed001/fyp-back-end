import wikipediaapi

wiki_wiki = wikipediaapi.Wikipedia('en')
# page_py = wiki_wiki.page(value)

page_py = wiki_wiki.page('Python_(programming_language)')

page_py = wiki_wiki.page('Blue Sapphire')
print("Page - Exists: %s" % page_py.exists())

# Page - Exists: False

print("Page - Summary: %s" % page_py.summary[0:60])