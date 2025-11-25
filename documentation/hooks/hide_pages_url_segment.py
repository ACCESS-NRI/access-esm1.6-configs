# Change the URL segment for pages in MkDocs to hide the "/pages" prefix, so that pages inside the
# "pages" directory are served directly at the root URL.
from mkdocs.plugins import event_priority
@event_priority(100)
def on_files(files, config):
    for file in files:
        file.dest_uri = file.dest_uri.removeprefix("pages/")